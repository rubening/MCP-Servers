import sys
import os

# Add the src directory to Python path
sys.path.insert(0, 'src')

# Compare original vs optimized
with open('optimization_comparison.txt', 'w') as f:
    try:
        from document_analyzer import DocumentAnalyzer
        analyzer = DocumentAnalyzer()
        
        f.write("=== PROJECT KNOWLEDGE OPTIMIZATION COMPARISON ===\n\n")
        
        # Analyze original
        if os.path.exists('project_knowledge.md'):
            original = analyzer.analyze_file('project_knowledge.md')
            f.write("ORIGINAL DOCUMENT:\n")
            f.write(f"  Overall Score: {original.overall_score}/100\n")
            f.write(f"  Structure: {original.scores['structure']}/100\n")
            f.write(f"  Content: {original.scores['content']}/100\n")
            f.write(f"  Clarity: {original.scores['clarity']}/100\n")
            f.write(f"  Context: {original.scores['context']}/100\n")
            f.write(f"  Total Words: {original.metrics['total_words']}\n")
            f.write(f"  Sections: {original.metrics['total_sections']}\n\n")
        
        # Analyze optimized
        if os.path.exists('project_knowledge_optimized.md'):
            optimized = analyzer.analyze_file('project_knowledge_optimized.md')
            f.write("OPTIMIZED DOCUMENT:\n")
            f.write(f"  Overall Score: {optimized.overall_score}/100\n")
            f.write(f"  Structure: {optimized.scores['structure']}/100\n")
            f.write(f"  Content: {optimized.scores['content']}/100\n")
            f.write(f"  Clarity: {optimized.scores['clarity']}/100\n")
            f.write(f"  Context: {optimized.scores['context']}/100\n")
            f.write(f"  Total Words: {optimized.metrics['total_words']}\n")
            f.write(f"  Sections: {optimized.metrics['total_sections']}\n\n")
            
            # Calculate improvements
            if 'original' in locals():
                f.write("IMPROVEMENT ANALYSIS:\n")
                score_diff = optimized.overall_score - original.overall_score
                f.write(f"  Overall Score Change: {score_diff:+.1f} points\n")
                f.write(f"  Structure Change: {optimized.scores['structure'] - original.scores['structure']:+.1f}\n")
                f.write(f"  Content Change: {optimized.scores['content'] - original.scores['content']:+.1f}\n")
                f.write(f"  Clarity Change: {optimized.scores['clarity'] - original.scores['clarity']:+.1f}\n")
                f.write(f"  Context Change: {optimized.scores['context'] - original.scores['context']:+.1f}\n")
                
                word_reduction = original.metrics['total_words'] - optimized.metrics['total_words']
                word_percent = (word_reduction / original.metrics['total_words']) * 100
                f.write(f"  Word Count Reduction: {word_reduction} words ({word_percent:.1f}%)\n")
                
                section_reduction = original.metrics['total_sections'] - optimized.metrics['total_sections']
                f.write(f"  Section Reduction: {section_reduction} sections\n\n")
                
                f.write("OPTIMIZATION SUCCESS:\n")
                if score_diff > 0:
                    f.write(f"  âœ“ Quality improved by {score_diff:.1f} points\n")
                if word_reduction > 0:
                    f.write(f"  âœ“ Cognitive load reduced by {word_percent:.1f}%\n")
                if optimized.scores['content'] > original.scores['content']:
                    f.write(f"  âœ“ Content score improved (better 80/20 focus)\n")
                if section_reduction > 0:
                    f.write(f"  âœ“ Section complexity reduced\n")
                    
        f.write("\nANALYSIS COMPLETED SUCCESSFULLY!\n")
        
    except Exception as e:
        f.write(f"ERROR: {e}\n")
        import traceback
        f.write(f"Traceback:\n{traceback.format_exc()}\n")

print("Optimization comparison completed - check optimization_comparison.txt")
