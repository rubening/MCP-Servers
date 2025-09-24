#!/usr/bin/env python3
"""
Google Ads MCP Server
Implements Perry Marshall 80/20 Principle + Todd Brown Copywriting Framework
For IRS Tax Attorney Marketing Campaigns
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio
import mcp.types as types

# Perry Marshall 80/20 Audience Targeting
TAX_ATTORNEY_AUDIENCES = {
    "high_value_prospects": {
        "demographics": "Business owners, high earners ($250K+), real estate investors",
        "pain_points": ["IRS audits", "tax penalties", "business tax optimization", "estate planning"],
        "ad_spend_allocation": "80%",  # 80/20 principle
        "expected_conversion": "20% of traffic, 80% of revenue"
    },
    "problem_aware": {
        "demographics": "Individuals with active IRS problems",
        "pain_points": ["tax liens", "wage garnishment", "unfiled returns", "payment plans"],
        "ad_spend_allocation": "15%",
        "expected_conversion": "Higher volume, lower value"
    },
    "solution_aware": {
        "demographics": "People researching tax attorneys",
        "pain_points": ["choosing the right attorney", "cost concerns", "case complexity"],
        "ad_spend_allocation": "5%",
        "expected_conversion": "Comparison shoppers"
    }
}

# Todd Brown Copywriting Framework
COPYWRITING_TEMPLATES = {
    "problem_promise_mechanism": {
        "structure": "PROBLEM: Most [target] struggle with [specific challenge] because [why current approaches fail]. PROMISE: What if you could [specific outcome] in [timeframe] without [major objection]? MECHANISM: The [unique method] makes this possible by [how it works] so that [why it works better].",
        "tax_attorney_example": "PROBLEM: Most business owners struggle with IRS problems because they try to handle complex tax issues themselves or hire inexperienced preparers. PROMISE: What if you could resolve your IRS problem in 30-90 days without paying more than necessary? MECHANISM: The Tax Resolution System makes this possible by leveraging 20+ years of IRS negotiation experience so that you get the best possible outcome faster than trying to negotiate yourself."
    },
    "headline_formulas": [
        "The [TIME] trick that [SPECIFIC BENEFIT]",
        "Why [COMMON PROBLEM] and how to [FIX IT]",
        "[NUMBER] [TIME FRAME] left to [BENEFIT/AVOID PAIN]",
        "Is [CURRENT SITUATION] costing you [SPECIFIC LOSS]?"
    ],
    "emotional_triggers": [
        "fear_of_irs_consequences",
        "relief_from_tax_stress", 
        "financial_security_restoration",
        "professional_credibility_protection"
    ]
}

# High-Converting Headlines for Tax Attorneys
TAX_ATTORNEY_HEADLINES = [
    "Stop IRS Collection Actions in 24 Hours (Even If You Owe $100K+)",
    "The 3-Step System That Reduces Tax Debt by 70% (IRS-Approved Method)",
    "Why Hiring a Tax Attorney Costs Less Than Doing Nothing",
    "Former IRS Agent Reveals: How to Beat Any Tax Problem Legally",
    "Warning: These 5 IRS Mistakes Could Cost You Everything",
    "How to Settle $50K Tax Debt for $5K (Real Case Study Inside)",
    "The IRS Collection Process Stopped Cold (Without Bankruptcy)",
    "Why 73% of Taxpayers Overpay the IRS (And How to Avoid It)",
    "Tax Lien Removed in 30 Days Using This Little-Known Loophole",
    "The Offer in Compromise Secret IRS Agents Don't Want You to Know"
]

# Campaign Templates
CAMPAIGN_TEMPLATES = {
    "irs_problem_resolution": {
        "target_audience": "high_value_prospects",
        "campaign_type": "Search + Display",
        "keywords": ["irs problem", "tax attorney", "irs audit", "tax debt relief"],
        "ad_groups": [
            {
                "name": "IRS Audit Defense",
                "keywords": ["irs audit attorney", "audit representation", "irs audit help"],
                "headlines": [
                    "Beat Your IRS Audit",
                    "Expert Audit Defense", 
                    "IRS Audit Attorney"
                ]
            },
            {
                "name": "Tax Debt Resolution", 
                "keywords": ["tax debt relief", "irs payment plan", "settle tax debt"],
                "headlines": [
                    "Reduce Tax Debt 70%",
                    "IRS Payment Plans",
                    "Tax Debt Settlement"
                ]
            }
        ]
    }
}

server = Server("google-ads-mcp")

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available Google Ads campaign resources."""
    return [
        Resource(
            uri="campaigns://tax-attorney-templates",
            name="Tax Attorney Campaign Templates",
            description="Pre-built campaign templates for IRS tax attorney marketing",
            mimeType="application/json"
        ),
        Resource(
            uri="audiences://80-20-targeting",
            name="80/20 Audience Targeting",
            description="Perry Marshall 80/20 principle applied to tax attorney audiences",
            mimeType="application/json"
        ),
        Resource(
            uri="copy://todd-brown-framework",
            name="Todd Brown Copywriting Framework", 
            description="High-converting copy framework for tax attorney ads",
            mimeType="application/json"
        ),
        Resource(
            uri="headlines://tax-attorney",
            name="Tax Attorney Headlines",
            description="Proven high-converting headlines for tax attorney campaigns",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read specific campaign resource content."""
    if uri == "campaigns://tax-attorney-templates":
        return json.dumps(CAMPAIGN_TEMPLATES, indent=2)
    elif uri == "audiences://80-20-targeting":
        return json.dumps(TAX_ATTORNEY_AUDIENCES, indent=2)
    elif uri == "copy://todd-brown-framework":
        return json.dumps(COPYWRITING_TEMPLATES, indent=2)
    elif uri == "headlines://tax-attorney":
        return json.dumps(TAX_ATTORNEY_HEADLINES, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available Google Ads campaign generation tools."""
    return [
        Tool(
            name="generate_campaign",
            description="Generate complete Google Ads campaign using Perry Marshall 80/20 + Todd Brown copywriting",
            inputSchema={
                "type": "object",
                "properties": {
                    "practice_area": {
                        "type": "string",
                        "description": "Tax attorney practice area (e.g., 'IRS Problem Resolution', 'Business Tax Planning')",
                        "default": "IRS Problem Resolution"
                    },
                    "budget": {
                        "type": "number",
                        "description": "Monthly advertising budget",
                        "default": 10000
                    },
                    "location": {
                        "type": "string", 
                        "description": "Geographic targeting location",
                        "default": "United States"
                    },
                    "awareness_level": {
                        "type": "string",
                        "enum": ["problem_unaware", "problem_aware", "solution_aware", "product_aware"],
                        "description": "Target audience awareness level for messaging",
                        "default": "problem_aware"
                    }
                },
                "required": ["practice_area"]
            }
        ),
        Tool(
            name="generate_ad_set",
            description="Generate ad group with Todd Brown copywriting framework",
            inputSchema={
                "type": "object",
                "properties": {
                    "ad_group_theme": {
                        "type": "string",
                        "description": "Main theme for ad group (e.g., 'IRS Audit Defense', 'Tax Debt Settlement')"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Target keywords for ad group"
                    },
                    "copywriting_focus": {
                        "type": "string",
                        "enum": ["problem_promise_mechanism", "social_proof", "urgency_scarcity", "authority_positioning"],
                        "description": "Primary copywriting approach",
                        "default": "problem_promise_mechanism"
                    }
                },
                "required": ["ad_group_theme", "keywords"]
            }
        ),
        Tool(
            name="generate_headlines",
            description="Generate high-converting headlines using proven formulas",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Specific tax issue or service to create headlines for"
                    },
                    "headline_type": {
                        "type": "string",
                        "enum": ["curiosity_benefit", "problem_solution", "urgency_specific", "question_hook"],
                        "description": "Type of headline formula to use",
                        "default": "problem_solution"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of headlines to generate",
                        "default": 10
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="analyze_80_20_performance",
            description="Analyze campaign performance using Perry Marshall 80/20 principles",
            inputSchema={
                "type": "object",
                "properties": {
                    "campaign_data": {
                        "type": "object",
                        "description": "Campaign performance metrics (impressions, clicks, conversions, cost)",
                        "properties": {
                            "impressions": {"type": "number"},
                            "clicks": {"type": "number"},
                            "conversions": {"type": "number"},
                            "cost": {"type": "number"}
                        }
                    },
                    "time_period": {
                        "type": "string",
                        "description": "Analysis time period",
                        "default": "last_30_days"
                    }
                },
                "required": ["campaign_data"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool execution for Google Ads campaign generation."""
    
    if name == "generate_campaign":
        practice_area = arguments.get("practice_area", "IRS Problem Resolution")
        budget = arguments.get("budget", 10000)
        location = arguments.get("location", "United States")
        awareness_level = arguments.get("awareness_level", "problem_aware")
        
        # Apply 80/20 budget allocation
        high_value_budget = budget * 0.8
        problem_aware_budget = budget * 0.15
        solution_aware_budget = budget * 0.05
        
        campaign = {
            "campaign_name": f"{practice_area} - Tax Attorney Marketing",
            "total_budget": budget,
            "location_targeting": location,
            "audience_awareness": awareness_level,
            "budget_allocation": {
                "high_value_prospects": f"${high_value_budget:,.0f} (80%)",
                "problem_aware": f"${problem_aware_budget:,.0f} (15%)", 
                "solution_aware": f"${solution_aware_budget:,.0f} (5%)"
            },
            "campaign_structure": {
                "search_campaigns": [
                    {
                        "name": f"{practice_area} - Search",
                        "budget": high_value_budget * 0.6,
                        "keywords": ["tax attorney", "irs problem", "tax debt relief", "irs audit"],
                        "match_types": ["exact", "phrase", "broad modifier"]
                    }
                ],
                "display_campaigns": [
                    {
                        "name": f"{practice_area} - Display",
                        "budget": high_value_budget * 0.4,
                        "targeting": "in-market audiences, custom intent audiences",
                        "placements": "financial websites, news sites, business publications"
                    }
                ]
            },
            "todd_brown_messaging": {
                "problem": f"Most business owners struggle with {practice_area.lower()} because they try to handle complex tax issues themselves or hire inexperienced preparers.",
                "promise": "What if you could resolve your IRS problem in 30-90 days without paying more than necessary?",
                "mechanism": "The Tax Resolution System makes this possible by leveraging 20+ years of IRS negotiation experience so that you get the best possible outcome faster than trying to negotiate yourself."
            }
        }
        
        return [types.TextContent(
            type="text",
            text=f"# Complete Google Ads Campaign: {practice_area}\n\n" +
                 f"## Perry Marshall 80/20 Budget Allocation\n" +
                 f"**Total Budget:** ${budget:,}/month\n" +
                 f"**High-Value Prospects:** ${high_value_budget:,.0f} (80%) - Business owners, high earners\n" +
                 f"**Problem-Aware Prospects:** ${problem_aware_budget:,.0f} (15%) - Active IRS problems\n" +
                 f"**Solution-Aware Prospects:** ${solution_aware_budget:,.0f} (5%) - Researching attorneys\n\n" +
                 f"## Todd Brown Messaging Framework\n" +
                 f"**Problem:** {campaign['todd_brown_messaging']['problem']}\n\n" +
                 f"**Promise:** {campaign['todd_brown_messaging']['promise']}\n\n" +
                 f"**Mechanism:** {campaign['todd_brown_messaging']['mechanism']}\n\n" +
                 f"## Campaign Structure\n" +
                 f"```json\n{json.dumps(campaign, indent=2)}\n```"
        )]
        
    elif name == "generate_ad_set":
        ad_group_theme = arguments["ad_group_theme"]
        keywords = arguments["keywords"]
        copywriting_focus = arguments.get("copywriting_focus", "problem_promise_mechanism")
        
        if copywriting_focus == "problem_promise_mechanism":
            ad_copy = {
                "headlines": [
                    f"Stop {ad_group_theme} Problems in 24 Hours",
                    f"Expert {ad_group_theme} Attorney",
                    f"Resolve {ad_group_theme} Fast"
                ],
                "descriptions": [
                    f"Former IRS agent with 20+ years experience. Free consultation. Stop {ad_group_theme.lower()} stress today.",
                    f"Don't face {ad_group_theme.lower()} alone. Expert legal representation. Call now for immediate help."
                ],
                "problem": f"Most people struggle with {ad_group_theme.lower()} because they don't know their rights or proper procedures.",
                "promise": f"You can resolve your {ad_group_theme.lower()} situation quickly with expert legal representation.",
                "mechanism": f"Our proven {ad_group_theme} system leverages decades of IRS experience to get the best outcome."
            }
        
        ad_set = {
            "ad_group_name": ad_group_theme,
            "keywords": keywords,
            "keyword_match_types": {
                "exact": [f'"{kw}"' for kw in keywords[:3]],
                "phrase": [f'"{kw}"' for kw in keywords[3:6]],
                "broad_modifier": [f'+{kw.replace(" ", " +")}'  for kw in keywords[6:]]
            },
            "ad_copy": ad_copy,
            "copywriting_framework": copywriting_focus,
            "bid_strategy": "Target CPA with $200 target (adjust based on client lifetime value)",
            "quality_score_optimization": [
                "Use keywords in headlines",
                "Match ad copy to landing page content",
                "Include emotional triggers and urgency",
                "Test different call-to-action phrases"
            ]
        }
        
        return [types.TextContent(
            type="text", 
            text=f"# Ad Group: {ad_group_theme}\n\n" +
                 f"## Keywords & Match Types\n" +
                 f"**Exact Match:** {', '.join(ad_set['keyword_match_types']['exact'])}\n" +
                 f"**Phrase Match:** {', '.join(ad_set['keyword_match_types']['phrase'])}\n" +
                 f"**Broad Modifier:** {', '.join(ad_set['keyword_match_types']['broad_modifier'])}\n\n" +
                 f"## Todd Brown Copy Framework\n" +
                 f"**Headlines:**\n" + '\n'.join(f"- {h}" for h in ad_copy['headlines']) + "\n\n" +
                 f"**Descriptions:**\n" + '\n'.join(f"- {d}" for d in ad_copy['descriptions']) + "\n\n" +
                 f"**Problem-Promise-Mechanism:**\n" +
                 f"- **Problem:** {ad_copy['problem']}\n" +
                 f"- **Promise:** {ad_copy['promise']}\n" +
                 f"- **Mechanism:** {ad_copy['mechanism']}\n\n" +
                 f"## Implementation Details\n" +
                 f"```json\n{json.dumps(ad_set, indent=2)}\n```"
        )]
        
    elif name == "generate_headlines":
        topic = arguments["topic"]
        headline_type = arguments.get("headline_type", "problem_solution")
        count = arguments.get("count", 10)
        
        headline_formulas = {
            "curiosity_benefit": [
                f"The [TIME] trick that stops {topic}",
                f"Why [EXPERT] never worry about {topic}",
                f"The secret to solving {topic} (that nobody talks about)",
                f"What [BIG COMPANY] knows about {topic} that you don't"
            ],
            "problem_solution": [
                f"Stop {topic} in 24 Hours (Even If You Owe $100K+)",
                f"Why {topic} happens and how to fix it permanently", 
                f"The 3-step system that eliminates {topic} fast",
                f"How to beat {topic} without expensive lawyers"
            ],
            "urgency_specific": [
                f"48 hours left to resolve {topic} (before it gets worse)",
                f"Last chance to stop {topic} penalties",
                f"Time running out on {topic} solutions",
                f"Don't let {topic} cost you everything"
            ],
            "question_hook": [
                f"Is {topic} costing you sleep at night?",
                f"What would life be like without {topic} stress?",
                f"Ready to eliminate {topic} forever?",
                f"Tired of {topic} controlling your life?"
            ]
        }
        
        selected_formulas = headline_formulas.get(headline_type, headline_formulas["problem_solution"])
        
        headlines = []
        for i in range(count):
            base_formula = selected_formulas[i % len(selected_formulas)]
            # Customize formula for the specific topic
            if "[TIME]" in base_formula:
                times = ["17-second", "30-day", "5-minute", "overnight"]
                formula = base_formula.replace("[TIME]", times[i % len(times)])
            elif "[EXPERT]" in base_formula:
                experts = ["tax attorneys", "former IRS agents", "tax professionals", "CPA firms"]
                formula = base_formula.replace("[EXPERT]", experts[i % len(experts)])
            elif "[BIG_COMPANY]" in base_formula:
                companies = ["the IRS", "Fortune 500 companies", "top law firms", "major corporations"]
                formula = base_formula.replace("[BIG_COMPANY]", companies[i % len(companies)])
            else:
                formula = base_formula
                
            headlines.append(formula)
        
        return [types.TextContent(
            type="text",
            text=f"# {count} High-Converting Headlines for: {topic}\n\n" +
                 f"## Headline Type: {headline_type.replace('_', ' ').title()}\n\n" +
                 '\n'.join(f"{i+1}. {headline}" for i, headline in enumerate(headlines)) + "\n\n" +
                 f"## Usage Notes:\n" +
                 f"- Test 3-5 headlines per ad group\n" +
                 f"- Rotate headlines every 2 weeks\n" +
                 f"- Monitor CTR and Quality Score\n" +
                 f"- A/B test different headline types\n" +
                 f"- Use top performers for landing pages"
        )]
        
    elif name == "analyze_80_20_performance":
        campaign_data = arguments["campaign_data"]
        time_period = arguments.get("time_period", "last_30_days")
        
        impressions = campaign_data.get("impressions", 0)
        clicks = campaign_data.get("clicks", 0) 
        conversions = campaign_data.get("conversions", 0)
        cost = campaign_data.get("cost", 0)
        
        # Calculate key metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
        cpc = (cost / clicks) if clicks > 0 else 0
        cost_per_conversion = (cost / conversions) if conversions > 0 else 0
        
        # 80/20 Analysis
        analysis = {
            "performance_metrics": {
                "ctr": f"{ctr:.2f}%",
                "conversion_rate": f"{conversion_rate:.2f}%", 
                "cpc": f"${cpc:.2f}",
                "cost_per_conversion": f"${cost_per_conversion:.2f}"
            },
            "80_20_insights": {
                "top_20_percent_performance": "Identify your highest performing 20% of keywords/ads that drive 80% of results",
                "budget_reallocation": "Shift more budget to top 20% of performers",
                "keyword_optimization": "Pause bottom 80% of keywords that generate <20% of conversions",
                "ad_copy_focus": "Scale winning ad copy variations that outperform"
            },
            "recommendations": []
        }
        
        # Generate specific recommendations based on performance
        if ctr < 2:
            analysis["recommendations"].append("CTR below 2% - Test more compelling headlines and emotional triggers")
        if conversion_rate < 3:
            analysis["recommendations"].append("Conversion rate below 3% - Optimize landing page messaging alignment")
        if cost_per_conversion > 500:
            analysis["recommendations"].append("High cost per conversion - Focus budget on highest converting keywords only")
            
        return [types.TextContent(
            type="text",
            text=f"# 80/20 Performance Analysis - {time_period}\n\n" +
                 f"## Campaign Metrics\n" +
                 f"- **Impressions:** {impressions:,}\n" +
                 f"- **Clicks:** {clicks:,}\n" +
                 f"- **Conversions:** {conversions:,}\n" +
                 f"- **Cost:** ${cost:,}\n" +
                 f"- **CTR:** {ctr:.2f}%\n" +
                 f"- **Conversion Rate:** {conversion_rate:.2f}%\n" +
                 f"- **CPC:** ${cpc:.2f}\n" +
                 f"- **Cost Per Conversion:** ${cost_per_conversion:.2f}\n\n" +
                 f"## 80/20 Optimization Strategy\n" +
                 f"**Focus on the 20% that drives 80% of results:**\n" +
                 f"- Identify top 20% of keywords by conversion volume\n" +
                 f"- Increase bids on highest ROI terms\n" +
                 f"- Pause underperforming bottom 80% of keywords\n" +
                 f"- Scale winning ad copy to more ad groups\n\n" +
                 f"## Specific Recommendations\n" +
                 '\n'.join(f"- {rec}" for rec in analysis["recommendations"]) + "\n\n" +
                 f"## Next Steps\n" +
                 f"1. Export keyword performance data\n" +
                 f"2. Sort by conversion volume (descending)\n" +
                 f"3. Identify top 20% performers\n" +
                 f"4. Reallocate 80% of budget to top performers\n" +
                 f"5. Test new ad variations for winning keywords"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
