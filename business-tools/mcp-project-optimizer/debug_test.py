import sys
import os

# Write output directly to a file to bypass console issues
with open('debug_output.txt', 'w') as f:
    f.write("=== DEBUG OUTPUT ===\n")
    f.write(f"Python version: {sys.version}\n")
    f.write(f"Working directory: {os.getcwd()}\n")
    f.write(f"Files in directory: {os.listdir('.')}\n")
    
    # Test if we can find our src directory
    if os.path.exists('src'):
        f.write("âœ“ Found src directory\n")
        f.write(f"  Files in src: {os.listdir('src')}\n")
        
        # Try to import our analyzer
        sys.path.insert(0, 'src')
        try:
            from document_analyzer import DocumentAnalyzer
            f.write("âœ“ DocumentAnalyzer imported successfully\n")
            
            # Test analysis
            if os.path.exists('sample_project_knowledge.md'):
                f.write("âœ“ Sample file found\n")
                
                analyzer = DocumentAnalyzer()
                result = analyzer.analyze_file('sample_project_knowledge.md')
                
                f.write(f"âœ“ Analysis completed!\n")
                f.write(f"  Overall score: {result.overall_score}/100\n")
                f.write(f"  Structure: {result.scores['structure']}/100\n")
                f.write(f"  Content: {result.scores['content']}/100\n")
                f.write(f"  Clarity: {result.scores['clarity']}/100\n")
                f.write(f"  Context: {result.scores['context']}/100\n")
                f.write(f"  Total words: {result.metrics['total_words']}\n")
                f.write(f"  Sections: {result.metrics['total_sections']}\n")
                f.write(f"  Recommendations: {len(result.recommendations)}\n")
                
                f.write("\nTop 3 recommendations:\n")
                for i, rec in enumerate(result.recommendations[:3], 1):
                    f.write(f"  {i}. {rec}\n")
                
                f.write("\nðŸŽ‰ SUCCESS: Core analyzer is working perfectly!\n")
            else:
                f.write("âœ— Sample file not found\n")
                
        except Exception as e:
            f.write(f"âœ— Error: {e}\n")
            import traceback
            f.write(f"Traceback:\n{traceback.format_exc()}\n")
    else:
        f.write("âœ— No src directory found\n")
    
    f.write("=== END DEBUG ===\n")

print("Debug completed - check debug_output.txt")
