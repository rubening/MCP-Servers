#!/usr/bin/env python3
"""
Command-line interface for the MCP Project Knowledge Optimizer

This script provides a simple way to analyze project_knowledge.md files
and get immediate feedback on quality and optimization opportunities.

Usage:
    python analyzer.py path/to/project_knowledge.md
    python analyzer.py --help
"""

import sys
import argparse
from pathlib import Path
from document_analyzer import DocumentAnalyzer, AnalysisResult


def create_analysis_report(result: AnalysisResult, file_path: str) -> str:
    """Create a comprehensive analysis report as a string"""
    
    report = []
    report.append("="*60)
    report.append("  MCP PROJECT KNOWLEDGE OPTIMIZER")
    report.append("  AI-Effectiveness Analysis Report")
    report.append("="*60)
    report.append(f"\nFile Analyzed: {file_path}")
    report.append("-" * 50)
    
    # Overall Score with status
    score = result.overall_score
    if score >= 80:
        status = "EXCELLENT [PASS]"
    elif score >= 70:
        status = "GOOD [PASS]"
    elif score >= 60:
        status = "NEEDS IMPROVEMENT [WARN]"
    else:
        status = "POOR [FAIL]"
        
    report.append(f"\nOVERALL QUALITY SCORE: {score}/100 ({status})")
    
    # Detailed Scores
    report.append(f"\nDETAILED SCORES:")
    report.append(f"   Structure:    {result.scores['structure']}/100")
    report.append(f"   Content:      {result.scores['content']}/100") 
    report.append(f"   Clarity:      {result.scores['clarity']}/100")
    report.append(f"   Context:      {result.scores['context']}/100")
    
    # Key Metrics
    report.append(f"\nKEY METRICS:")
    metrics = result.metrics
    report.append(f"   Total Words:     {metrics['total_words']}")
    report.append(f"   Sections:        {metrics['total_sections']}")
    report.append(f"   Max Section:     {metrics['max_section_words']} words")
    report.append(f"   Avg Section:     {metrics['avg_section_words']} words")
    report.append(f"   Header Depth:    {metrics['hierarchy_depth']} levels")
    report.append(f"   Code Blocks:     {'Yes' if metrics['has_code_blocks'] else 'No'}")
    report.append(f"   Appendices:      {'Yes' if metrics['has_appendices'] else 'No'}")
    
    # Recommendations
    report.append(f"\nRECOMMENDATIONS ({len(result.recommendations)} items):")
    if result.recommendations:
        for i, rec in enumerate(result.recommendations, 1):
            report.append(f"   {i}. {rec}")
    else:
        report.append("   No recommendations - document is well optimized!")
    
    # Section Breakdown
    report.append(f"\nSECTION BREAKDOWN:")
    for i, section in enumerate(result.sections, 1):
        level_indent = "  " * (section['level'] - 1)
        status_icon = "[LONG]" if section['word_count'] > 750 else "[OK]"
        report.append(f"   {i}. {level_indent}H{section['level']}: {section['title']}")
        report.append(f"      {level_indent}Words: {section['word_count']} {status_icon}")
    
    # Tips
    report.append(f"\nOPTIMIZATION TIPS:")
    report.append("   - Keep sections under 750 words for better readability")
    report.append("   - Target 1,000-2,000 total words for optimal AI effectiveness") 
    report.append("   - Start with context: project overview, tech stack, constraints")
    report.append("   - Use bullet points and code blocks for clarity")
    report.append("   - Move detailed info to appendix sections")
    report.append("   - Limit header nesting to 4 levels maximum")
    
    report.append(f"\nAnalysis completed successfully!")
    report.append("="*60)
    
    return "\n".join(report)


def analyze_file(file_path: str) -> bool:
    """
    Analyze a single file and return success status
    
    Args:
        file_path: Path to the project_knowledge.md file
        
    Returns:
        True if analysis succeeded, False otherwise
    """
    try:
        # Create analyzer
        analyzer = DocumentAnalyzer()
        
        # Run analysis
        result = analyzer.analyze_file(file_path)
        
        # Create report
        report = create_analysis_report(result, file_path)
        
        # Write to both console and file
        print(report)
        
        # Also save to a report file
        report_filename = f"analysis_report_{Path(file_path).stem}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {report_filename}")
        
        return True
        
    except FileNotFoundError:
        error_msg = f"ERROR: Could not find file: {file_path}\nMake sure the file path is correct and the file exists."
        print(error_msg)
        return False
        
    except Exception as e:
        error_msg = f"ERROR: Analysis failed: {e}"
        print(error_msg)
        return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Analyze and optimize project_knowledge.md files for AI effectiveness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyzer.py project_knowledge.md
  python analyzer.py ../my-project/project_knowledge.md

This tool analyzes your project documentation and provides:
- Quality scores across multiple dimensions
- Specific recommendations for improvement  
- Detailed metrics and section breakdown
- Tips for optimizing AI collaboration effectiveness
        """
    )
    
    parser.add_argument(
        'file_path',
        help='Path to the project_knowledge.md file to analyze'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='MCP Project Knowledge Optimizer v1.0.0'
    )
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return
        
    args = parser.parse_args()
    
    # Validate file path
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"ERROR: File does not exist: {args.file_path}")
        print("Please check the file path and try again.")
        sys.exit(1)
        
    if not file_path.is_file():
        print(f"ERROR: Path is not a file: {args.file_path}")
        sys.exit(1)
    
    # Run analysis
    success = analyze_file(str(file_path))
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
