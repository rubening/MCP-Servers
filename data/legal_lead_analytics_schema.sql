-- Legal Lead Analytics Schema for Ruben's CRM Data
-- Optimized for CallRail + ActiveCampaign integration

CREATE TABLE IF NOT EXISTS lead_interactions (
    id VARCHAR PRIMARY KEY,
    source_system VARCHAR, -- 'CallRail' or 'ActiveCampaign'
    interaction_type VARCHAR, -- 'Call' or 'WebForm'
    
    -- Contact Info (normalized)
    phone_normalized VARCHAR,
    email VARCHAR,
    name_full VARCHAR,
    name_first VARCHAR,
    name_last VARCHAR,
    
    -- Timing
    interaction_datetime TIMESTAMP,
    day_of_week VARCHAR,
    
    -- UTM Tracking  
    utm_source VARCHAR,
    utm_medium VARCHAR,
    utm_campaign VARCHAR,
    utm_content VARCHAR,
    utm_term VARCHAR,
    
    -- URLs
    landing_page_url VARCHAR,
    referring_url VARCHAR,
    
    -- Device & Location
    device VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR,
    
    -- Call Specific
    call_duration INTEGER,
    call_answered BOOLEAN,
    call_recording_url VARCHAR,
    
    -- Form Specific  
    form_type VARCHAR,
    form_message TEXT,
    
    -- ClickUp Integration
    clickup_contact_task_id VARCHAR,
    clickup_interaction_task_id VARCHAR,
    
    -- Business Intelligence
    created_at TIMESTAMP DEFAULT NOW(),
    lead_value_score INTEGER, -- calculated field
    conversion_probability FLOAT -- ML prediction
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_source_system ON lead_interactions(source_system);
CREATE INDEX IF NOT EXISTS idx_interaction_date ON lead_interactions(interaction_datetime);
CREATE INDEX IF NOT EXISTS idx_utm_campaign ON lead_interactions(utm_campaign);
CREATE INDEX IF NOT EXISTS idx_conversion_prob ON lead_interactions(conversion_probability);

-- Views for common queries
CREATE VIEW IF NOT EXISTS daily_lead_summary AS
SELECT 
    DATE(interaction_datetime) as date,
    source_system,
    COUNT(*) as total_leads,
    COUNT(CASE WHEN interaction_type = 'Call' THEN 1 END) as calls,
    COUNT(CASE WHEN interaction_type = 'WebForm' THEN 1 END) as webforms,
    AVG(lead_value_score) as avg_lead_score
FROM lead_interactions 
GROUP BY DATE(interaction_datetime), source_system
ORDER BY date DESC;

CREATE VIEW IF NOT EXISTS utm_performance AS
SELECT 
    utm_campaign,
    utm_source,
    utm_medium,
    COUNT(*) as leads,
    AVG(conversion_probability) as avg_conversion_rate,
    COUNT(CASE WHEN call_answered = true THEN 1 END) as answered_calls
FROM lead_interactions 
WHERE utm_campaign IS NOT NULL
GROUP BY utm_campaign, utm_source, utm_medium
ORDER BY leads DESC;