"""
Legal Lead Analytics Integrator
Connects Ruben's n8n CRM automation with DuckDB business intelligence

Takes normalized lead data from n8n workflow and creates comprehensive analytics
"""

import duckdb
import json
from datetime import datetime
from typing import Dict, Any, Optional

class LegalLeadAnalytics:
    def __init__(self, db_path: str = "C:\\Users\\ruben\\Claude Tools\\analytics\\business_intelligence.db"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables if they don't exist"""
        with open("C:\\Users\\ruben\\Claude Tools\\analytics\\legal_lead_analytics_schema.sql", 'r') as f:
            schema_sql = f.read()
        self.conn.execute(schema_sql)
    
    def process_n8n_lead(self, normalized_data: Dict[str, Any]) -> str:
        """
        Process normalized lead data from n8n workflow
        Expected format matches your data normalizer output
        """
        
        # Extract data from n8n normalized format
        contact = normalized_data.get('contact', {})
        phone = contact.get('phone', {})
        name = contact.get('name', {})
        time = normalized_data.get('time', {})
        utm = normalized_data.get('utm', {})
        urls = normalized_data.get('urls', {})
        additional = normalized_data.get('additionalData', {})
        
        # Generate unique ID
        lead_id = f"{normalized_data.get('sourceSystem', 'UNK')}_{additional.get('sourceUniqueId', '')}_{ datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate lead value score (basic algorithm)
        lead_score = self._calculate_lead_score(normalized_data)
        
        # Insert into database
        insert_sql = """
        INSERT INTO lead_interactions (
            id, source_system, interaction_type,
            phone_normalized, email, name_full, name_first, name_last,
            interaction_datetime, day_of_week,
            utm_source, utm_medium, utm_campaign, utm_content, utm_term,
            landing_page_url, referring_url,
            device, customer_city, customer_state,
            call_duration, call_answered, call_recording_url,
            form_type, form_message,
            lead_value_score, conversion_probability
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            lead_id,
            normalized_data.get('sourceSystem', ''),
            normalized_data.get('interactionType', ''),
            phone.get('normalized', ''),
            contact.get('email', ''),
            name.get('full', ''),
            name.get('first', ''),
            name.get('last', ''),
            time.get('iso', None),
            time.get('dayOfWeek', ''),
            utm.get('source', ''),
            utm.get('medium', ''),
            utm.get('campaign', ''),
            utm.get('content', ''),
            utm.get('term', ''),
            urls.get('landing', ''),
            urls.get('referring', ''),
            normalized_data.get('device', ''),
            additional.get('customerCity', ''),
            additional.get('customerState', ''),
            self._safe_int(additional.get('callDuration')),
            additional.get('callAnswered'),
            additional.get('callRecording', ''),
            additional.get('formType', ''),
            additional.get('message', ''),
            lead_score,
            self._calculate_conversion_probability(normalized_data)
        )
        
        self.conn.execute(insert_sql, values)
        return lead_id
    
    def _calculate_lead_score(self, data: Dict[str, Any]) -> int:
        """Calculate lead quality score 1-100"""
        score = 50  # base score
        
        # Phone number quality
        phone = data.get('contact', {}).get('phone', {})
        if phone.get('normalized'):
            score += 15
        
        # Email presence
        if data.get('contact', {}).get('email'):
            score += 10
        
        # Name completeness
        name = data.get('contact', {}).get('name', {})
        if name.get('first') and name.get('last'):
            score += 10
        
        # Business hours (higher value)
        time_str = data.get('time', {}).get('display', '')
        if any(hour in time_str for hour in ['9am', '10am', '11am', '1pm', '2pm', '3pm', '4pm']):
            score += 10
        
        # UTM tracking (indicates marketing attribution)
        utm = data.get('utm', {})
        if utm.get('campaign') or utm.get('source'):
            score += 5
        
        # Call answered (CallRail specific)
        if data.get('additionalData', {}).get('callAnswered'):
            score += 20
        
        return min(score, 100)
    
    def _calculate_conversion_probability(self, data: Dict[str, Any]) -> float:
        """Simple conversion probability model"""
        base_prob = 0.15  # 15% base conversion rate
        
        # Adjust based on factors
        if data.get('sourceSystem') == 'CallRail' and data.get('additionalData', {}).get('callAnswered'):
            base_prob += 0.25  # Answered calls convert much better
        
        if data.get('contact', {}).get('name', {}).get('first') and data.get('contact', {}).get('name', {}).get('last'):
            base_prob += 0.10  # Complete names indicate serious interest
        
        return min(base_prob, 0.95)
    
    def _safe_int(self, value) -> Optional[int]:
        """Safely convert to int"""
        if value is None or value == '':
            return None
        try:
            return int(float(str(value)))
        except:
            return None
    
    def get_daily_summary(self, days: int = 30) -> list:
        """Get daily lead summary for last N days"""
        sql = """
        SELECT * FROM daily_lead_summary 
        WHERE date >= CURRENT_DATE - INTERVAL '{}' DAYS
        ORDER BY date DESC
        """.format(days)
        return self.conn.execute(sql).fetchall()
    
    def get_utm_performance(self) -> list:
        """Get UTM campaign performance"""
        return self.conn.execute("SELECT * FROM utm_performance").fetchall()
    
    def get_conversion_insights(self) -> Dict[str, Any]:
        """Get business intelligence insights"""
        insights = {}
        
        # Overall conversion rates
        overall = self.conn.execute("""
            SELECT 
                source_system,
                COUNT(*) as total_leads,
                AVG(conversion_probability) as avg_conversion_rate,
                AVG(lead_value_score) as avg_lead_score
            FROM lead_interactions 
            GROUP BY source_system
        """).fetchall()
        insights['overall'] = overall
        
        # Best performing times
        time_performance = self.conn.execute("""
            SELECT 
                day_of_week,
                COUNT(*) as leads,
                AVG(lead_value_score) as avg_score
            FROM lead_interactions 
            GROUP BY day_of_week 
            ORDER BY avg_score DESC
        """).fetchall()
        insights['time_performance'] = time_performance
        
        # Top campaigns
        top_campaigns = self.conn.execute("""
            SELECT 
                utm_campaign,
                COUNT(*) as leads,
                AVG(conversion_probability) as conversion_rate
            FROM lead_interactions 
            WHERE utm_campaign IS NOT NULL AND utm_campaign != ''
            GROUP BY utm_campaign 
            ORDER BY leads DESC 
            LIMIT 10
        """).fetchall()
        insights['top_campaigns'] = top_campaigns
        
        return insights

# Example usage function for n8n integration
def process_webhook_data(webhook_payload: str) -> str:
    """
    Function to call from n8n or other automation
    Takes JSON string, returns lead_id
    """
    try:
        data = json.loads(webhook_payload)
        analytics = LegalLeadAnalytics()
        lead_id = analytics.process_n8n_lead(data)
        return f"Lead processed: {lead_id}"
    except Exception as e:
        return f"Error processing lead: {str(e)}"

if __name__ == "__main__":
    # Test with sample data structure
    sample_data = {
        "sourceSystem": "CallRail",
        "interactionType": "Call",
        "contact": {
            "phone": {"normalized": "5551234567"},
            "email": "test@example.com",
            "name": {"full": "John Smith", "first": "John", "last": "Smith"}
        },
        "time": {"iso": "2025-06-15T10:30:00", "dayOfWeek": "Monday"},
        "utm": {"source": "google", "campaign": "tax-relief"},
        "additionalData": {"callAnswered": True, "callDuration": "120"}
    }
    
    analytics = LegalLeadAnalytics()
    lead_id = analytics.process_n8n_lead(sample_data)
    print(f"Processed lead: {lead_id}")
    
    # Get insights
    insights = analytics.get_conversion_insights()
    print("Conversion insights:", insights)
