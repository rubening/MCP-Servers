import sys
import os

# Add the src directory to Python path
sys.path.insert(0, 'src')

# Write output directly to a file to bypass console issues
with open('ruben_analysis_results.txt', 'w') as f:
    try:
        from document_analyzer import DocumentAnalyzer
        f.write("=== RUBEN'S PROJECT_KNOWLEDGE.MD ANALYSIS ===\n\n")
        
        if os.path.exists('project_knowledge.md'):
            analyzer = DocumentAnalyzer()
            result = analyzer.analyze_file('project_knowledge.md')
            
            f.write(f"OVERALL SCORE: {result.overall_score}/100\n")
            
            # Determine status
            score = result.overall_score
            if score >= 80:
                status = "EXCELLENT"
            elif score >= 70:
                status = "GOOD"
            elif score >= 60:
                status = "NEEDS IMPROVEMENT"
            else:
                status = "POOR"
            f.write(f"STATUS: {status}\n\n")
            
            f.write("DETAILED SCORES:\n")
            f.write(f"  Structure: {result.scores['structure']}/100\n")
            f.write(f"  Content:   {result.scores['content']}/100\n")
            f.write(f"  Clarity:   {result.scores['clarity']}/100\n")
            f.write(f"  Context:   {result.scores['context']}/100\n\n")
            
            f.write("KEY METRICS:\n")
            metrics = result.metrics
            f.write(f"  Total Words:     {metrics['total_words']}\n")
            f.write(f"  Sections:        {metrics['total_sections']}\n")
            f.write(f"  Max Section:     {metrics['max_section_words']} words\n")
            f.write(f"  Avg Section:     {metrics['avg_section_words']} words\n")
            f.write(f"  Header Depth:    {metrics['hierarchy_depth']} levels\n")
            f.write(f"  Code Blocks:     {'Yes' if metrics['has_code_blocks'] else 'No'}\n")
            f.write(f"  Appendices:      {'Yes' if metrics['has_appendices'] else 'No'}\n\n")
            
            f.write(f"RECOMMENDATIONS ({len(result.recommendations)} items):\n")
            for i, rec in enumerate(result.recommendations, 1):
                f.write(f"  {i}. {rec}\n")
            
            f.write(f"\nSUCCESS: Analysis of your real project_knowledge.md completed!\n")
            f.write(f"File size: {os.path.getsize('project_knowledge.md')} bytes\n")
            
        else:
            f.write("ERROR: project_knowledge.md not found\n")
            
    except Exception as e:
        f.write(f"ERROR: {e}\n")
        import traceback
        f.write(f"Traceback:\n{traceback.format_exc()}\n")

print("Analysis completed - check ruben_analysis_results.txt")
