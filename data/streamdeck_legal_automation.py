"""
Stream Deck Legal Analytics Automation
Connects Stream Deck buttons to legal lead analytics and ClickUp

Button Functions:
1. Daily Lead Report
2. UTM Campaign Performance  
3. Conversion Rate Analysis
4. ClickUp Task Summary
5. Live Lead Monitoring
"""

import json
import sys
from datetime import datetime, timedelta
from analytics.legal_lead_analytics_integrator import LegalLeadAnalytics
import subprocess

class StreamDeckLegalAutomation:
    def __init__(self):
        self.analytics = LegalLeadAnalytics()
    
    def daily_lead_report(self) -> str:
        """Generate daily lead report for Stream Deck display"""
        try:
            summary = self.analytics.get_daily_summary(days=7)
            
            report = "DAILY LEAD REPORT\\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            
            total_leads = 0
            total_calls = 0
            total_webforms = 0
            
            for day in summary[:7]:  # Last 7 days
                date, source, leads, calls, webforms, avg_score = day
                total_leads += leads
                total_calls += calls
                total_webforms += webforms
                
                report += f"{date}: {leads} leads ({calls}C/{webforms}W) Score:{avg_score:.1f}\\n"
            
            report += f"\\nWEEKLY TOTALS:\\n"
            report += f"Total Leads: {total_leads}\\n"
            report += f"Calls: {total_calls} | Web Forms: {total_webforms}\\n"
            
            # Save to file for Stream Deck to read
            with open("C:\\Users\\ruben\\Claude Tools\\analytics\\daily_report.txt", "w") as f:
                f.write(report.replace("\\n", "\n"))
            
            return report
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def utm_performance_report(self) -> str:
        """Generate UTM campaign performance report"""
        try:
            utm_data = self.analytics.get_utm_performance()
            
            report = "UTM CAMPAIGN PERFORMANCE\\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            
            for campaign, source, medium, leads, conversion_rate, answered_calls in utm_data[:10]:
                report += f"Campaign: {campaign}\\n"
                report += f"   Source: {source} | Medium: {medium}\\n"
                report += f"   Leads: {leads} | Conv Rate: {conversion_rate:.1%}\\n"
                report += f"   Answered Calls: {answered_calls}\\n\\n"
            
            with open("C:\\Users\\ruben\\Claude Tools\\analytics\\utm_report.txt", "w") as f:
                f.write(report.replace("\\n", "\n"))
            
            return report
            
        except Exception as e:
            return f"Error generating UTM report: {str(e)}"
    
    def conversion_insights_report(self) -> str:
        """Generate conversion insights report"""
        try:
            insights = self.analytics.get_conversion_insights()
            
            report = "CONVERSION INSIGHTS\\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            
            # Overall performance
            report += "OVERALL PERFORMANCE:\\n"
            for source, total, conversion_rate, lead_score in insights['overall']:
                report += f"{source}: {total} leads | {conversion_rate:.1%} conv | {lead_score:.0f} score\\n"
            
            # Best days
            report += "\\nBEST PERFORMING DAYS:\\n"
            for day, leads, score in insights['time_performance'][:3]:
                report += f"{day}: {leads} leads | {score:.0f} avg score\\n"
            
            # Top campaigns
            if insights['top_campaigns']:
                report += "\\nTOP CAMPAIGNS:\\n"
                for campaign, leads, conversion in insights['top_campaigns'][:3]:
                    report += f"{campaign}: {leads} leads | {conversion:.1%} conv\\n"
            
            with open("C:\\Users\\ruben\\Claude Tools\\analytics\\insights_report.txt", "w") as f:
                f.write(report.replace("\\n", "\n"))
            
            return report
            
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def live_lead_monitor(self) -> str:
        """Show recent leads for live monitoring"""
        try:
            recent_leads = self.analytics.conn.execute("""
                SELECT 
                    source_system, interaction_type, name_full, 
                    phone_normalized, interaction_datetime, lead_value_score
                FROM lead_interactions 
                WHERE interaction_datetime >= DATETIME('now', '-24 hours')
                ORDER BY interaction_datetime DESC 
                LIMIT 10
            """).fetchall()
            
            report = "LIVE LEAD MONITOR (24h)\\n"
            report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n"
            
            if not recent_leads:
                report += "No leads in last 24 hours\\n"
            else:
                for source, interaction, name, phone, datetime_str, score in recent_leads:
                    time_part = datetime_str.split('T')[1][:5] if 'T' in datetime_str else datetime_str
                    report += f"{interaction} | {name}\\n"
                    report += f"   {phone} | Score: {score} | {time_part}\\n\\n"
            
            with open("C:\\Users\\ruben\\Claude Tools\\analytics\\live_monitor.txt", "w") as f:
                f.write(report.replace("\\n", "\n"))
            
            return report
            
        except Exception as e:
            return f"Error monitoring leads: {str(e)}"

def main():
    """Main function for Stream Deck button execution"""
    if len(sys.argv) < 2:
        print("Usage: streamdeck_legal_automation.py [daily|utm|insights|live]")
        return
    
    automation = StreamDeckLegalAutomation()
    action = sys.argv[1].lower()
    
    if action == "daily":
        result = automation.daily_lead_report()
    elif action == "utm":
        result = automation.utm_performance_report()
    elif action == "insights":
        result = automation.conversion_insights_report()
    elif action == "live":
        result = automation.live_lead_monitor()
    else:
        result = "Unknown action. Use: daily, utm, insights, or live"
    
    print(result)
    
    # Optional: Open report file in default text viewer
    if action in ["daily", "utm", "insights", "live"]:
        report_file = f"C:\\Users\\ruben\\Claude Tools\\analytics\\{action}_report.txt"
        try:
            subprocess.run(["notepad.exe", report_file], check=False)
        except:
            pass  # Fail silently if notepad isn't available

if __name__ == "__main__":
    main()
