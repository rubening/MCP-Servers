"""
Test runner for the Document Analyzer - no external dependencies needed

This is a minimal test to verify our analyzer works without requiring
Python package installations.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Create a simple version of textstat for testing
class MockTextstat:
    @staticmethod
    def flesch_kincaid_reading_ease(text):
        # Simple approximation: more complex text = lower score
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        if sentences == 0 or words == 0:
            return 50
        
        # Rough approximation of readability
        avg_sentence_length = words / sentences
        if avg_sentence_length < 10:
            return 80  # Easy to read
        elif avg_sentence_length < 20:
            return 60  # Standard
        else:
            return 40  # Difficult

# Mock the textstat module
sys.modules['textstat'] = MockTextstat()

# Now import our analyzer
from document_analyzer import DocumentAnalyzer

def test_analyzer():
    """Test the analyzer with our sample file"""
    print("="*50)
    print("TESTING MCP PROJECT KNOWLEDGE OPTIMIZER")
    print("="*50)
    
    # Test file path
    sample_file = "sample_project_knowledge.md"
    
    if not os.path.exists(sample_file):
        print(f"ERROR: Cannot find {sample_file}")
        print("Make sure you're running this from the mcp-project-optimizer directory")
        return False
    
    try:
        # Create analyzer
        analyzer = DocumentAnalyzer()
        print(f"\nAnalyzing: {sample_file}")
        print("Running analysis modules...")
        
        # Run analysis
        result = analyzer.analyze_file(sample_file)
        
        # Print results
        print(f"\nANALYSIS RESULTS")
        print("-" * 30)
        
        # Overall Score
        score = result.overall_score
        if score >= 80:
            status = "EXCELLENT"
        elif score >= 70:
            status = "GOOD"
        elif score >= 60:
            status = "NEEDS IMPROVEMENT"
        else:
            status = "POOR"
            
        print(f"\nOVERALL QUALITY SCORE: {score}/100 ({status})")
        
        # Detailed Scores
        print(f"\nDETAILED SCORES:")
        print(f"   Structure:    {result.scores['structure']}/100")
        print(f"   Content:      {result.scores['content']}/100") 
        print(f"   Clarity:      {result.scores['clarity']}/100")
        print(f"   Context:      {result.scores['context']}/100")
        
        # Key Metrics
        print(f"\nKEY METRICS:")
        metrics = result.metrics
        print(f"   Total Words:     {metrics['total_words']}")
        print(f"   Sections:        {metrics['total_sections']}")
        print(f"   Max Section:     {metrics['max_section_words']} words")
        print(f"   Avg Section:     {metrics['avg_section_words']} words")
        print(f"   Header Depth:    {metrics['hierarchy_depth']} levels")
        print(f"   Code Blocks:     {'Yes' if metrics['has_code_blocks'] else 'No'}")
        print(f"   Appendices:      {'Yes' if metrics['has_appendices'] else 'No'}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS ({len(result.recommendations)} items):")
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   No recommendations - document is well optimized!")
        
        print(f"\nSUCCESS: Analysis completed successfully!")
        print(f"\nThis demonstrates the core analysis engine is working.")
        print(f"Next steps: Install Python dependencies for full functionality.")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analyzer()
