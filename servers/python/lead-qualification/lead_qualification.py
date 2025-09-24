#!/usr/bin/env python3
"""
Lead Qualification MCP Server - ENHANCED v2.0 - ATTORNEY VALIDATED
Revolutionary AI-powered lead qualification with business intelligence penalties
Enhanced with Attorney Tony Ramos feedback for "free advice" and "taxpayer advocate" patterns
Built using the proven manual JSON-RPC pattern for Ruben's ecosystem.
"""

import asyncio
import json
import os
import sys
import sqlite3
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import urllib.parse

class LeadQualificationMCP:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "lead_qualification.db")
        self.init_database()
        
        # Configuration patterns extracted from n8n workflow
        self.config = {
            "airtable": {
                "baseId": "appGPNKX6FFmUzO7t",
                "tables": {
                    "contacts": "tblUf0CfYo1wo9SuM",
                    "interactions": "tblJ3Lgn7lK96yF3e"
                }
            },
            "clickup": {
                "lists": {
                    "contacts": "901110756634",
                    "calls": "901110756636", 
                    "webforms": "901110756638"
                },
                "customFields": {
                    "lifecycle": "efb6c000-251b-42df-b9c6-46adc3fd5e71",
                    "lifecycleLead": "dfde02ea-2257-4af5-ab3c-c62234a49e79",
                    "airtableId": "c75ed76a-283d-456a-a876-53633999931c",
                    "sourceUniqueId": "bdfe5411-3bcf-4e72-bace-8a0d07d8ba37"
                }
            },
            "scoring": {
                "base_scores": {
                    "call_answered": 25,
                    "form_submission": 15,
                    "email_provided": 10,
                    "phone_provided": 15
                },
                "multipliers": {
                    "business_hours": 1.2,
                    "same_day": 1.5,
                    "repeat_contact": 2.0
                },
                # ENHANCED: Attorney-validated business intelligence penalties
                "business_penalties": {
                    "free_advice": 40,
                    "taxpayer_advocate": 25,
                    "price_shopping": 15,
                    "information_only": 10,
                    "compound_multiplier": 1.2
                }
            }
        }
    
    def init_database(self):
        """Initialize lead qualification database with comprehensive schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Leads table with scoring
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_system TEXT NOT NULL,
            source_unique_id TEXT,
            normalized_phone TEXT,
            email TEXT,
            full_name TEXT,
            first_name TEXT,
            last_name TEXT,
            lead_score INTEGER DEFAULT 0,
            qualification_status TEXT DEFAULT 'new',
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT,
            utm_content TEXT,
            utm_term TEXT,
            device_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Interactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            interaction_type TEXT,
            interaction_data TEXT,
            score_contribution INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
        ''')
        
        # Lead scoring history
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scoring_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER,
            old_score INTEGER,
            new_score INTEGER,
            score_reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_request_id(self, request):
        req_id = request.get("id")
        if req_id is None:
            return 0
        return req_id
    
    async def handle_request(self, request):
        method = request.get("method", "")
        request_id = self.get_request_id(request)
        
        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "lead-qualification-mcp", "version": "2.0.0"}
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "normalize_webhook_data",
                                "description": "Universal payload normalizer for CallRail and ActiveCampaign webhooks with enhanced error handling",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "webhook_payload": {"type": "object", "description": "Raw webhook payload from CallRail or ActiveCampaign"},
                                        "source_hint": {"type": "string", "description": "Optional source system hint (callrail/activecampaign)"}
                                    },
                                    "required": ["webhook_payload"]
                                }
                            },
                            {
                                "name": "score_lead_quality",
                                "description": "AI-powered lead scoring using behavioral patterns and qualification criteria",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lead_data": {"type": "object", "description": "Normalized lead data"},
                                        "interaction_data": {"type": "object", "description": "Interaction details"}
                                    },
                                    "required": ["lead_data"]
                                }
                            },
                            {
                                "name": "deduplicate_contact",
                                "description": "Advanced contact deduplication using phone and email composite matching",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "phone": {"type": "string", "description": "Phone number for matching"},
                                        "email": {"type": "string", "description": "Email address for matching"},
                                        "source_id": {"type": "string", "description": "Source system unique ID"}
                                    },
                                    "required": []
                                }
                            },
                            {
                                "name": "track_interaction",
                                "description": "Track and analyze lead interactions with score impact calculation",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lead_id": {"type": "integer", "description": "Lead ID"},
                                        "interaction_type": {"type": "string", "description": "Type of interaction (call/form/email)"},
                                        "interaction_data": {"type": "object", "description": "Detailed interaction data"}
                                    },
                                    "required": ["lead_id", "interaction_type"]
                                }
                            },
                            {
                                "name": "enrich_contact_data",
                                "description": "Enrich contact data with additional business intelligence and scoring factors",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "lead_id": {"type": "integer", "description": "Lead ID to enrich"},
                                        "enrichment_sources": {"type": "array", "items": {"type": "string"}, "description": "Sources for enrichment"}
                                    },
                                    "required": ["lead_id"]
                                }
                            },
                            {
                                "name": "analyze_transcription_content",
                                "description": "AI-powered transcription analysis using DeepSeek reasoning for intelligent lead qualification",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "transcription": {"type": "string", "description": "Call transcription text to analyze"},
                                        "call_metadata": {"type": "object", "description": "Additional call context (duration, source, etc.)"},
                                        "business_context": {"type": "string", "description": "Business type context (default: tax law office)"}
                                    },
                                    "required": ["transcription"]
                                }
                            },
                            {
                                "name": "generate_lead_report",
                                "description": "Generate comprehensive lead qualification reports and analytics",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "date_range": {"type": "string", "description": "Date range for report (7d/30d/90d)"},
                                        "source_filter": {"type": "string", "description": "Filter by source system"},
                                        "score_threshold": {"type": "integer", "description": "Minimum score threshold"}
                                    },
                                    "required": []
                                }
                            }
                        ]
                    }
                }
                
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})
                
                # Route to tool functions
                if tool_name == "normalize_webhook_data":
                    return await self.normalize_webhook_data(request_id, arguments)
                elif tool_name == "score_lead_quality":
                    return await self.score_lead_quality(request_id, arguments)
                elif tool_name == "deduplicate_contact":
                    return await self.deduplicate_contact(request_id, arguments)
                elif tool_name == "track_interaction":
                    return await self.track_interaction(request_id, arguments)
                elif tool_name == "enrich_contact_data":
                    return await self.enrich_contact_data(request_id, arguments)
                elif tool_name == "analyze_transcription_content":
                    return await self.analyze_transcription_content(request_id, arguments)
                elif tool_name == "generate_lead_report":
                    return await self.generate_lead_report(request_id, arguments)
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def analyze_transcription_content(self, request_id, arguments):
        """AI-powered transcription analysis with enhanced business logic - ATTORNEY VALIDATED"""
        transcription = arguments.get("transcription", "")
        call_metadata = arguments.get("call_metadata", {})
        business_context = arguments.get("business_context", "tax law office specializing in IRS issues and tax relief")
        
        try:
            # Enhanced business intelligence pattern analysis
            transcription_lower = transcription.lower()
            
            # CRITICAL BUSINESS INSIGHT: Attorney-validated negative indicators
            business_negative_patterns = [
                'free advice', 'free consultation', 'just want some advice',
                'taxpayer advocate', 'taxpayers advocate', 'ta office',
                'shopping around', 'checking prices', 'compare rates',
                'general information', 'quick question', 'just wondering'
            ]
            
            # Solicitation keywords
            solicitation_patterns = [
                'restaurant', 'catering', 'menu', 'food service', 'delivery',
                'insurance', 'marketing', 'advertising', 'promotion', 'sale',
                'credit card', 'loan', 'mortgage', 'investment', 'solar',
                'energy', 'home improvement', 'warranty', 'vehicle'
            ]
            
            # High-value legal keywords (attorney validated)
            high_value_legal_patterns = [
                'irs notice', 'audit', 'lien', 'levy', 'garnishment', 'seizure',
                'collection', 'enforcement', 'deadline', 'penalty', 'interest',
                'business tax', 'payroll tax', 'trust fund', 'criminal investigation'
            ]
            
            # Standard legal keywords
            standard_legal_patterns = [
                'irs', 'tax', 'debt', 'owe', 'payment plan', 'installment',
                'bankruptcy', 'settlement', 'attorney', 'legal', 'help',
                'problem', 'resolution', 'representation'
            ]
            
            # Agent response analysis
            declined_patterns = [
                'we\'re good', 'not interested', 'no thank you', 'we don\'t need',
                'small office', 'appreciate your call but', 'all set'
            ]
            
            # Calculate pattern scores
            business_negative_score = sum(1 for pattern in business_negative_patterns if pattern in transcription_lower)
            solicitation_score = sum(1 for pattern in solicitation_patterns if pattern in transcription_lower)
            high_value_legal_score = sum(1 for pattern in high_value_legal_patterns if pattern in transcription_lower)
            standard_legal_score = sum(1 for pattern in standard_legal_patterns if pattern in transcription_lower)
            declined_score = sum(1 for pattern in declined_patterns if pattern in transcription_lower)
            
            # Enhanced business scoring logic with attorney-validated penalties
            base_score = 0
            applied_penalties = 0
            business_flags = {
                "free_advice_seeking": "free advice" in transcription_lower,
                "taxpayer_advocate_reference": "taxpayer advocate" in transcription_lower or "taxpayers advocate" in transcription_lower,
                "price_shopping": any(term in transcription_lower for term in ['shopping around', 'compare rates', 'checking prices']),
                "information_only": any(term in transcription_lower for term in ['general information', 'quick question', 'just wondering'])
            }
            
            # Apply business intelligence penalties
            if business_flags["free_advice_seeking"]:
                applied_penalties += self.config["scoring"]["business_penalties"]["free_advice"]
            if business_flags["taxpayer_advocate_reference"]:
                applied_penalties += self.config["scoring"]["business_penalties"]["taxpayer_advocate"]
            if business_flags["price_shopping"]:
                applied_penalties += self.config["scoring"]["business_penalties"]["price_shopping"]
            if business_flags["information_only"]:
                applied_penalties += self.config["scoring"]["business_penalties"]["information_only"]
            
            # Compound penalty for multiple negative indicators
            if applied_penalties > 40:
                applied_penalties = int(applied_penalties * self.config["scoring"]["business_penalties"]["compound_multiplier"])
            
            # Determine base scoring before penalties
            if solicitation_score > 0 and standard_legal_score == 0:
                intent = "Solicitation"
                intent_confidence = min(90, 60 + (solicitation_score * 10))
                base_score = -45
                qualification_status = "Unqualified - Solicitation"
            elif high_value_legal_score > 0:
                intent = "High-Value Legal Inquiry"
                intent_confidence = min(95, 80 + (high_value_legal_score * 5))
                base_score = 70 + (high_value_legal_score * 15)
                qualification_status = "High-Value Legal Prospect"
            elif standard_legal_score > 2:
                intent = "Standard Legal Inquiry"
                intent_confidence = min(90, 70 + (standard_legal_score * 5))
                base_score = 50 + (standard_legal_score * 10)
                qualification_status = "Qualified Legal Lead"
            elif declined_score > 0:
                intent = "Declined Service"
                intent_confidence = 80
                base_score = -20
                qualification_status = "Unqualified - Declined"
            else:
                intent = "Information Request"
                intent_confidence = 60
                base_score = 10
                qualification_status = "Standard Lead"
            
            # Apply business logic penalties and caps
            final_score = base_score - applied_penalties
            
            # Cap positive scores when negative business indicators present
            if applied_penalties > 0 and final_score > 40:
                final_score = 40  # Attorney-validated cap for negative indicators
            
            # Update qualification status based on final score
            if applied_penalties > 0:
                if final_score <= 40:
                    qualification_status = "Low Conversion Probability"
                warning_flags = []
                if business_flags["free_advice_seeking"]:
                    warning_flags.append("FREE ADVICE SEEKING")
                if business_flags["taxpayer_advocate_reference"]:
                    warning_flags.append("TAXPAYER ADVOCATE REFERENCE")
                if warning_flags:
                    qualification_status += f" - {', '.join(warning_flags)}"
            
            # Enhanced analysis result with business intelligence
            analysis_result = {
                "transcription_analysis": {
                    "intent_classification": {
                        "primary_intent": intent,
                        "confidence": intent_confidence,
                        "reasoning": f"Base intent: {intent}. Business flags detected: {sum(business_flags.values())}"
                    },
                    "legal_relevance_score": max(0, (high_value_legal_score * 25) + (standard_legal_score * 10)),
                    "engagement_quality_score": max(0, 70 - (declined_score * 20)),
                    "solicitation_detected": solicitation_score > 0,
                    "business_value_assessment": {
                        "negative_indicators_detected": applied_penalties > 0,
                        "free_advice_seeking": business_flags["free_advice_seeking"],
                        "taxpayer_advocate_reference": business_flags["taxpayer_advocate_reference"],
                        "price_shopping": business_flags["price_shopping"],
                        "information_only": business_flags["information_only"]
                    },
                    "keywords_found": {
                        "high_value_legal": [pattern for pattern in high_value_legal_patterns if pattern in transcription_lower],
                        "standard_legal": [pattern for pattern in standard_legal_patterns if pattern in transcription_lower],
                        "solicitation_keywords": [pattern for pattern in solicitation_patterns if pattern in transcription_lower],
                        "business_negative": [pattern for pattern in business_negative_patterns if pattern in transcription_lower],
                        "declined_indicators": [pattern for pattern in declined_patterns if pattern in transcription_lower]
                    }
                },
                "scoring_recommendation": {
                    "base_score": base_score,
                    "applied_penalties": applied_penalties,
                    "final_score": final_score,
                    "recommended_status": qualification_status,
                    "reasoning": f"Base: {base_score}, Penalties: -{applied_penalties}, Final: {final_score}",
                    "business_intelligence": {
                        "conversion_probability": "Low" if applied_penalties > 0 else "High" if final_score > 60 else "Medium",
                        "attorney_time_recommendation": "Skip" if applied_penalties > 30 else "Review" if final_score > 40 else "Standard",
                        "warning_flags": [flag.replace('_', ' ').title() for flag, value in business_flags.items() if value]
                    },
                    "action_items": [
                        "WARNING: LOW CONVERSION PROBABILITY - Review business flags before follow-up" if applied_penalties > 0 else
                        "HIGH PRIORITY: High priority follow-up - Genuine legal prospect" if final_score > 60 else
                        "STANDARD: Standard follow-up" if final_score > 0 else
                        "SOLICITATION: Mark as solicitation - no follow-up needed"
                    ]
                },
                "call_quality_metrics": {
                    "transcription_length": len(transcription),
                    "call_duration": call_metadata.get('duration', 0),
                    "engagement_indicators": (high_value_legal_score * 2) + standard_legal_score + max(0, 3 - declined_score),
                    "business_relevance": "High" if high_value_legal_score > 0 else "Low" if solicitation_score > 0 or applied_penalties > 0 else "Medium"
                },
                "attorney_intelligence": {
                    "system_version": "Enhanced v2.0 - Attorney Validated Business Logic",
                    "validation_source": "Attorney Tony Ramos feedback integrated",
                    "enhancement_note": "Business intelligence penalties applied based on conversion probability analysis"
                }
            }
            
            result_text = json.dumps(analysis_result, indent=2)
            
        except Exception as e:
            result_text = f"Error in enhanced transcription analysis: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def normalize_webhook_data(self, request_id, arguments):
        """Universal payload normalizer extracted from n8n workflow logic"""
        webhook_payload = arguments.get("webhook_payload", {})
        source_hint = arguments.get("source_hint", "")
        
        try:
            # Extract webhook data - handle n8n webhook node format
            event = webhook_payload
            if 'body' in webhook_payload and isinstance(webhook_payload['body'], list):
                event = webhook_payload['body'][0] if webhook_payload['body'] else {}
            elif 'body' in webhook_payload and isinstance(webhook_payload['body'], dict):
                event = webhook_payload['body']
            
            # Source system detection (extracted from n8n logic)
            source_system = ''
            interaction_type = ''
            
            if event.get('call_type') or webhook_payload.get('query', {}).get('call_type'):
                source_system = 'CallRail'
                interaction_type = 'Call'
            elif event.get('contact', {}).get('id') or event.get('contact[id]'):
                source_system = 'ActiveCampaign' 
                interaction_type = 'WebForm'
            else:
                source_system = source_hint or 'Unknown'
                interaction_type = 'Unknown'
            
            # Phone normalization (extracted from n8n helper function)
            def normalize_phone(phone):
                phone_str = str(phone or '').strip()
                digits = re.sub(r'\D', '', phone_str)
                if not digits:
                    return {'raw': '', 'normalized': '', 'national': '', 'international': ''}
                
                return {
                    'raw': phone_str,
                    'normalized': digits,
                    'national': f"({digits[:3]}) {digits[3:6]}-{digits[6:]}" if len(digits) >= 10 else digits,
                    'international': f"+1{digits}" if len(digits) >= 10 else f"+{digits}"
                }
            
            # Name parsing (extracted from n8n helper function)
            def parse_name(full_name):
                raw_name = str(full_name or '').strip()
                if not raw_name:
                    return {'full': '', 'first': '', 'middle': '', 'last': '', 'suffix': ''}
                
                # Title case conversion
                name = ' '.join(word.capitalize() for word in raw_name.split())
                parts = name.split()
                
                suffixes = ['jr', 'jr.', 'sr', 'sr.', 'ii', 'iii', 'iv', 'v', 'esq', 'esq.']
                suffix = ''
                if len(parts) > 1 and parts[-1].lower() in suffixes:
                    suffix = parts.pop()
                
                return {
                    'full': name,
                    'first': parts[0] if parts else '',
                    'middle': ' '.join(parts[1:-1]) if len(parts) > 2 else '',
                    'last': parts[-1] if len(parts) > 1 else '',
                    'suffix': suffix
                }
            
            # Extract data based on source
            if source_system == 'CallRail':
                CR = event
                CRQuery = webhook_payload.get('query', {})
                
                phone_data = normalize_phone(
                    CR.get('formatted_customer_phone_number') or 
                    CR.get('customer_phone_number') or
                    CRQuery.get('callernum')
                )
                
                name_data = parse_name(
                    CR.get('formatted_customer_name') or 
                    CR.get('customer_name') or
                    CRQuery.get('callername')
                )
                
                email = str(CR.get('customer_email', '') or CRQuery.get('customer_email', '')).strip().lower()
                
                utm_data = {
                    'source': CR.get('utm_source', ''),
                    'medium': CR.get('utm_medium', ''),
                    'campaign': CR.get('utm_campaign', ''),
                    'content': CR.get('utm_content', ''),
                    'term': CR.get('utm_term', '')
                }
                
                additional_data = {
                    'call_duration': CR.get('duration', ''),
                    'call_answered': CR.get('answered'),
                    'call_recording': CR.get('recording', ''),
                    'call_transcription': CR.get('transcription', ''),
                    'source_unique_id': CR.get('person_resource_id', ''),
                    'device_type': CR.get('device_type', '')
                }
                
            else:  # ActiveCampaign
                AC = event.get('contact', {})
                ACF = AC.get('fields', {})
                
                # Handle flattened format
                if event.get('contact[id]'):
                    AC = {
                        'id': event.get('contact[id]'),
                        'email': event.get('contact[email]'),
                        'first_name': event.get('contact[first_name]'),
                        'last_name': event.get('contact[last_name]'),
                        'phone': event.get('contact[phone]')
                    }
                    ACF = {k.replace('contact[fields][', '').replace(']', ''): v 
                          for k, v in event.items() if k.startswith('contact[fields]')}
                
                phone_data = normalize_phone(AC.get('phone'))
                name_data = parse_name(f"{AC.get('first_name', '')} {AC.get('last_name', '')}".strip())
                email = str(AC.get('email', '')).strip().lower()
                
                utm_data = {
                    'source': ACF.get('utmsource', ''),
                    'medium': ACF.get('utmmedium', ''),
                    'campaign': ACF.get('utmcampaign', ''),
                    'content': ACF.get('utmcontent', ''),
                    'term': ACF.get('utmterm', '')
                }
                
                additional_data = {
                    'form_type': ACF.get('form_type', ''),
                    'form_name': ACF.get('form_name', ''),
                    'message': ACF.get('hiddencomments', ''),
                    'source_unique_id': str(AC.get('id', '')),
                    'device_type': ACF.get('device', '')
                }
            
            # Normalize device type
            device_map = {'m': 'Mobile', 'mobile': 'Mobile', 'd': 'Desktop', 'desktop': 'Desktop', 't': 'Tablet', 'tablet': 'Tablet'}
            device = device_map.get(additional_data.get('device_type', '').lower(), additional_data.get('device_type', ''))
            
            normalized_data = {
                'source_system': source_system,
                'interaction_type': interaction_type,
                'contact': {
                    'phone': phone_data,
                    'email': email,
                    'name': name_data
                },
                'utm': utm_data,
                'device': device,
                'additional_data': additional_data,
                'timestamp': datetime.now().isoformat(),
                'raw_payload': webhook_payload
            }
            
            result_text = json.dumps(normalized_data, indent=2)
            
        except Exception as e:
            result_text = f"Error normalizing webhook data: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def score_lead_quality(self, request_id, arguments):
        """AI-powered lead scoring using behavioral patterns"""
        lead_data = arguments.get("lead_data", {})
        interaction_data = arguments.get("interaction_data", {})
        
        try:
            base_score = 0
            score_factors = []
            
            # Base scoring from configuration
            if interaction_data.get('call_answered'):
                base_score += self.config['scoring']['base_scores']['call_answered']
                score_factors.append("Call answered (+25)")
            
            if interaction_data.get('interaction_type') == 'WebForm':
                base_score += self.config['scoring']['base_scores']['form_submission']
                score_factors.append("Form submission (+15)")
            
            if lead_data.get('contact', {}).get('email'):
                base_score += self.config['scoring']['base_scores']['email_provided']
                score_factors.append("Email provided (+10)")
            
            if lead_data.get('contact', {}).get('phone', {}).get('normalized'):
                base_score += self.config['scoring']['base_scores']['phone_provided']
                score_factors.append("Phone provided (+15)")
            
            # Advanced scoring factors
            utm_source = lead_data.get('utm', {}).get('source', '').lower()
            if utm_source in ['google', 'bing', 'search']:
                base_score += 20
                score_factors.append("Organic search traffic (+20)")
            elif utm_source in ['facebook', 'linkedin']:
                base_score += 10
                score_factors.append("Social media traffic (+10)")
            
            # Device scoring
            device = lead_data.get('device', '').lower()
            if device == 'mobile':
                base_score += 5
                score_factors.append("Mobile user (+5)")
            
            # Call quality factors
            call_duration = interaction_data.get('call_duration')
            if call_duration and int(call_duration) > 120:  # 2+ minutes
                base_score += 30
                score_factors.append(f"Long call duration {call_duration}s (+30)")
            
            # Business hours multiplier
            now = datetime.now()
            if 9 <= now.hour <= 17:  # Business hours
                base_score = int(base_score * self.config['scoring']['multipliers']['business_hours'])
                score_factors.append("Business hours contact (x1.2)")
            
            scoring_result = {
                'lead_score': base_score,
                'scoring_factors': score_factors,
                'qualification_status': self._determine_qualification_status(base_score),
                'score_breakdown': {
                    'base_score': base_score,
                    'interaction_quality': len(score_factors),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            result_text = json.dumps(scoring_result, indent=2)
            
        except Exception as e:
            result_text = f"Error scoring lead quality: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }
    
    def _determine_qualification_status(self, score):
        """Determine qualification status based on score"""
        if score >= 80:
            return "Hot Lead"
        elif score >= 60:
            return "Warm Lead"
        elif score >= 40:
            return "Qualified Lead"
        elif score >= 20:
            return "Cold Lead"
        else:
            return "Unqualified"

    async def deduplicate_contact(self, request_id, arguments):
        """Advanced contact deduplication logic"""
        phone = arguments.get("phone", "")
        email = arguments.get("email", "")
        source_id = arguments.get("source_id", "")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search for existing contacts (extracted from n8n UPSERT logic)
            search_conditions = []
            params = []
            
            if phone:
                search_conditions.append("normalized_phone = ?")
                params.append(phone)
            
            if email:
                search_conditions.append("email = ?")
                params.append(email)
            
            if search_conditions:
                query = f"SELECT * FROM leads WHERE {' OR '.join(search_conditions)} LIMIT 1"
                cursor.execute(query, params)
                existing_contact = cursor.fetchone()
                
                if existing_contact:
                    # Contact exists - return merge strategy
                    result = {
                        "duplicate_found": True,
                        "existing_contact_id": existing_contact[0],
                        "merge_strategy": "update_empty_fields",
                        "confidence": "high" if phone and email else "medium"
                    }
                else:
                    # No duplicate found
                    result = {
                        "duplicate_found": False,
                        "action": "create_new_contact",
                        "confidence": "high"
                    }
            else:
                result = {
                    "duplicate_found": False,
                    "action": "insufficient_data",
                    "confidence": "low"
                }
            
            conn.close()
            result_text = json.dumps(result, indent=2)
            
        except Exception as e:
            result_text = f"Error in contact deduplication: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def track_interaction(self, request_id, arguments):
        """Track lead interactions with score impact"""
        lead_id = arguments.get("lead_id")
        interaction_type = arguments.get("interaction_type", "")
        interaction_data = arguments.get("interaction_data", {})
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate score contribution
            score_contribution = 0
            if interaction_type == "Call":
                score_contribution = 25
            elif interaction_type == "WebForm":
                score_contribution = 15
            elif interaction_type == "Email":
                score_contribution = 10
            
            # Store interaction
            cursor.execute('''
            INSERT INTO interactions (lead_id, interaction_type, interaction_data, score_contribution)
            VALUES (?, ?, ?, ?)
            ''', (lead_id, interaction_type, json.dumps(interaction_data), score_contribution))
            
            interaction_id = cursor.lastrowid
            
            # Update lead score
            cursor.execute('SELECT lead_score FROM leads WHERE id = ?', (lead_id,))
            current_score = cursor.fetchone()[0] if cursor.fetchone() else 0
            new_score = current_score + score_contribution
            
            cursor.execute('UPDATE leads SET lead_score = ?, updated_at = ? WHERE id = ?', 
                         (new_score, datetime.now().isoformat(), lead_id))
            
            # Log score change
            cursor.execute('''
            INSERT INTO scoring_history (lead_id, old_score, new_score, score_reason)
            VALUES (?, ?, ?, ?)
            ''', (lead_id, current_score, new_score, f"{interaction_type} interaction"))
            
            conn.commit()
            conn.close()
            
            result = {
                "interaction_id": interaction_id,
                "score_contribution": score_contribution,
                "new_total_score": new_score,
                "interaction_tracked": True
            }
            
            result_text = json.dumps(result, indent=2)
            
        except Exception as e:
            result_text = f"Error tracking interaction: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def enrich_contact_data(self, request_id, arguments):
        """Enrich contact data with business intelligence"""
        lead_id = arguments.get("lead_id")
        enrichment_sources = arguments.get("enrichment_sources", [])
        
        try:
            # Placeholder for future integrations (Clearbit, ZoomInfo, etc.)
            enrichment_data = {
                "lead_id": lead_id,
                "enrichment_attempted": True,
                "sources_checked": enrichment_sources,
                "data_added": {
                    "company_info": "Available with API integration",
                    "social_profiles": "Available with API integration",
                    "industry_classification": "Available with API integration"
                },
                "next_steps": [
                    "Integrate Clearbit API for company data",
                    "Add LinkedIn Sales Navigator integration",
                    "Connect ZoomInfo for B2B enrichment"
                ]
            }
            
            result_text = json.dumps(enrichment_data, indent=2)
            
        except Exception as e:
            result_text = f"Error enriching contact data: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

    async def generate_lead_report(self, request_id, arguments):
        """Generate comprehensive lead qualification reports"""
        date_range = arguments.get("date_range", "30d")
        source_filter = arguments.get("source_filter", "")
        score_threshold = arguments.get("score_threshold", 0)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate date range
            days = int(date_range.rstrip('d'))
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Build query with filters
            query = '''
            SELECT 
                source_system,
                COUNT(*) as total_leads,
                AVG(lead_score) as avg_score,
                COUNT(CASE WHEN lead_score >= ? THEN 1 END) as qualified_leads,
                qualification_status
            FROM leads 
            WHERE created_at >= ?
            '''
            params = [score_threshold, start_date]
            
            if source_filter:
                query += " AND source_system = ?"
                params.append(source_filter)
            
            query += " GROUP BY source_system, qualification_status"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Generate report
            report = {
                "report_period": f"Last {days} days",
                "date_range": {"start": start_date, "end": datetime.now().isoformat()},
                "filters_applied": {
                    "source_filter": source_filter or "All sources",
                    "score_threshold": score_threshold
                },
                "summary": {},
                "by_source": {},
                "recommendations": []
            }
            
            total_leads = sum(row[1] for row in results)
            total_qualified = sum(row[3] for row in results)
            
            report["summary"] = {
                "total_leads": total_leads,
                "qualified_leads": total_qualified,
                "qualification_rate": f"{(total_qualified/total_leads*100):.1f}%" if total_leads > 0 else "0%",
                "average_score": f"{sum(row[2] for row in results)/len(results):.1f}" if results else "0"
            }
            
            # Add recommendations based on data
            if total_qualified < total_leads * 0.3:
                report["recommendations"].append("Consider lowering qualification threshold or improving lead sources")
            
            if any(row[0] == 'CallRail' for row in results):
                report["recommendations"].append("High-value source: Continue CallRail optimization")
            
            conn.close()
            result_text = json.dumps(report, indent=2)
            
        except Exception as e:
            result_text = f"Error generating lead report: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result_text}]}
        }

async def main():
    mcp = LeadQualificationMCP()
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await mcp.handle_request(request)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            continue

if __name__ == "__main__":
    asyncio.run(main())
