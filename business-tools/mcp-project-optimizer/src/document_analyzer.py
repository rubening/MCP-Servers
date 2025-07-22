"""
Core Document Analyzer for Project Knowledge Files

This module provides the main DocumentAnalyzer class that coordinates
all analysis modules to generate a comprehensive quality score and 
recommendations for project_knowledge.md files.
"""

import re
import markdown
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Try to import textstat, use fallback if not available
try:
    import textstat
except ImportError:
    # Simple fallback for readability scoring
    class MockTextstat:
        @staticmethod
        def flesch_kincaid_reading_ease(text):
            # Simple approximation based on sentence and word length
            sentences = text.count('.') + text.count('!') + text.count('?')
            words = len(text.split())
            if sentences == 0 or words == 0:
                return 50
            
            avg_sentence_length = words / sentences
            if avg_sentence_length < 10:
                return 80  # Easy to read
            elif avg_sentence_length < 20:
                return 60  # Standard
            else:
                return 40  # Difficult
    
    textstat = MockTextstat()


@dataclass
class AnalysisResult:
    """Container for analysis results"""
    overall_score: float
    scores: Dict[str, float]
    recommendations: List[str]
    metrics: Dict[str, Any]
    sections: List[Dict[str, Any]]


class DocumentAnalyzer:
    """
    Main analyzer class that coordinates all document analysis modules
    
    This class implements the core analysis logic from the research-driven
    specification, focusing on the 80/20 principle, cognitive load optimization,
    and AI-effectiveness scoring.
    """
    
    def __init__(self):
        """Initialize analyzer with default configuration"""
        self.min_context_words = 500  # Minimum words for context section
        self.max_section_words = 750  # Maximum words per section
        self.ideal_total_words = 1500  # Sweet spot for total length
        self.max_hierarchy_depth = 4  # Maximum header nesting
        
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """
        Analyze a project_knowledge.md file and return comprehensive results
        
        Args:
            file_path: Path to the project_knowledge.md file
            
        Returns:
            AnalysisResult with scores, metrics, and recommendations
        """
        # Read the file
        content = self._read_file(file_path)
        
        # Parse the markdown structure
        sections = self._parse_sections(content)
        
        # Run all analysis modules
        structure_score = self._analyze_structure(sections)
        content_score = self._analyze_content(content, sections)
        clarity_score = self._analyze_clarity(content)
        context_score = self._analyze_context(sections)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            sections, structure_score, content_score, clarity_score, context_score
        )
        
        # Calculate overall score (weighted average)
        overall_score = (
            structure_score * 0.25 +  # Document organization
            content_score * 0.30 +    # Content quality and prioritization  
            clarity_score * 0.25 +    # Readability and cognitive load
            context_score * 0.20      # Context completeness
        )
        
        return AnalysisResult(
            overall_score=round(overall_score, 1),
            scores={
                'structure': round(structure_score, 1),
                'content': round(content_score, 1), 
                'clarity': round(clarity_score, 1),
                'context': round(context_score, 1)
            },
            recommendations=recommendations,
            metrics=self._calculate_metrics(content, sections),
            sections=sections
        )
    
    def _read_file(self, file_path: str) -> str:
        """Read file content with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find file: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    
    def _parse_sections(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse markdown content into sections based on headers
        
        Returns list of sections with metadata like header level, 
        word count, and content
        """
        sections = []
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            # Check if line is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)', line)
            if header_match:
                # Save previous section if exists
                if current_section:
                    current_section['word_count'] = len(current_section['content'].split())
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2)
                current_section = {
                    'level': level,
                    'title': title,
                    'content': '',
                    'line_number': len(sections) + 1
                }
            elif current_section:
                # Add content to current section
                current_section['content'] += line + '\n'
        
        # Don't forget the last section
        if current_section:
            current_section['word_count'] = len(current_section['content'].split())
            sections.append(current_section)
            
        return sections
    
    def _analyze_structure(self, sections: List[Dict[str, Any]]) -> float:
        """
        Analyze document structure quality
        
        Checks hierarchy depth, section balance, and logical organization
        """
        if not sections:
            return 0.0
            
        score = 100.0
        
        # Check hierarchy depth (penalize too deep nesting)
        max_depth = max(section['level'] for section in sections)
        if max_depth > self.max_hierarchy_depth:
            score -= (max_depth - self.max_hierarchy_depth) * 15
        
        # Check for logical header progression (no skipping levels)
        for i, section in enumerate(sections[1:], 1):
            prev_level = sections[i-1]['level']
            curr_level = section['level']
            if curr_level > prev_level + 1:  # Skipped a level
                score -= 10
        
        # Check section size balance
        oversized_sections = sum(1 for s in sections if s['word_count'] > self.max_section_words)
        score -= oversized_sections * 8
        
        # Bonus for having a good number of sections (not too few, not too many)
        section_count = len(sections)
        if 4 <= section_count <= 12:
            score += 10
        elif section_count < 4:
            score -= 15
        elif section_count > 20:
            score -= 10
            
        return max(0.0, min(100.0, score))
    
    def _analyze_content(self, content: str, sections: List[Dict[str, Any]]) -> float:
        """
        Analyze content quality using 80/20 principle
        
        Focuses on whether core content is properly prioritized and sized
        """
        total_words = len(content.split())
        score = 100.0
        
        # Check total length (sweet spot around 1500 words)
        if total_words < 800:
            score -= 20  # Too brief
        elif total_words > 3000:
            score -= 25  # Too verbose
        elif 1000 <= total_words <= 2000:
            score += 15  # In the sweet spot
            
        # Check for proper content prioritization
        # Look for sections that might be "core" vs "appendix"
        core_sections = [s for s in sections if s['level'] <= 2]
        appendix_sections = [s for s in sections if 'appendix' in s['title'].lower()]
        
        # Core sections should contain the bulk of important info
        core_words = sum(s['word_count'] for s in core_sections)
        if core_words / total_words > 0.8:  # 80/20 principle
            score += 10
        else:
            score -= 10
            
        # Bonus for having appendix/reference sections
        if appendix_sections:
            score += 5
            
        return max(0.0, min(100.0, score))
    
    def _analyze_clarity(self, content: str) -> float:
        """
        Analyze readability and cognitive load
        
        Uses established readability metrics and checks for clear writing
        """
        score = 100.0
        
        # Calculate readability score (Flesch-Kincaid)
        try:
            fk_score = textstat.flesch_kincaid_reading_ease(content)
            # Target: 60-70 (readable for technical audience)
            if 60 <= fk_score <= 70:
                score += 15
            elif 50 <= fk_score <= 80:
                score += 5
            elif fk_score < 30:  # Too difficult
                score -= 20
            elif fk_score > 90:  # Too simple for technical content
                score -= 10
        except:
            pass  # If textstat fails, skip this metric
        
        # Check average sentence length (target: 12-18 words)
        sentences = re.split(r'[.!?]+', content)
        sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
        if sentence_lengths:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            if 12 <= avg_length <= 18:
                score += 10
            elif avg_length > 25:
                score -= 15  # Too complex
                
        # Check for bullet points and lists (aid scanning)
        bullet_count = content.count('*') + content.count('-') + content.count('+')
        if bullet_count > 5:
            score += 5
            
        # Check for code blocks (important for technical docs)
        code_blocks = content.count('```')
        if code_blocks >= 2:  # At least one code block
            score += 5
            
        return max(0.0, min(100.0, score))
    
    def _analyze_context(self, sections: List[Dict[str, Any]]) -> float:
        """
        Analyze context completeness using context-first architecture principles
        
        Checks for the four required context elements in early sections
        """
        if not sections:
            return 0.0
            
        score = 100.0
        
        # Look for context indicators in first 3 sections
        context_sections = sections[:3] if len(sections) >= 3 else sections
        combined_context = ' '.join(s['content'].lower() for s in context_sections)
        
        # Check for required context elements
        context_elements = {
            'project_overview': ['project', 'goal', 'purpose', 'objective'],
            'technical_stack': ['technology', 'framework', 'language', 'stack', 'dependencies'],
            'constraints': ['requirement', 'constraint', 'compliance', 'security'],
            'decisions': ['decision', 'choice', 'rationale', 'why', 'because']
        }
        
        found_elements = 0
        for element_name, keywords in context_elements.items():
            if any(keyword in combined_context for keyword in keywords):
                found_elements += 1
                
        # Score based on how many context elements are present
        context_score = (found_elements / 4) * 100
        
        # Check if context section is substantial enough
        context_words = sum(s['word_count'] for s in context_sections)
        if context_words < self.min_context_words:
            score -= 30  # Insufficient context detail
        elif context_words > 1500:
            score -= 10   # Too much context (should be concise)
            
        # Combine context completeness with context size appropriateness
        final_score = (context_score * 0.7) + (score * 0.3)
        
        return max(0.0, min(100.0, final_score))
    
    def _generate_recommendations(self, sections, structure_score, content_score, clarity_score, context_score) -> List[str]:
        """Generate actionable recommendations based on analysis results"""
        recommendations = []
        
        # Structure recommendations
        if structure_score < 70:
            if any(s['level'] > 4 for s in sections):
                recommendations.append("STRUCTURE: Reduce header nesting - limit to 4 levels maximum for better readability")
            
            oversized = [s for s in sections if s['word_count'] > self.max_section_words]
            if oversized:
                recommendations.append(f"STRUCTURE: Break up large sections - {len(oversized)} sections exceed {self.max_section_words} words")
                
        # Content recommendations  
        if content_score < 70:
            total_words = sum(s['word_count'] for s in sections)
            if total_words < 1000:
                recommendations.append("CONTENT: Add more detail - document is too brief for effective AI collaboration")
            elif total_words > 2500:
                recommendations.append("CONTENT: Consider moving detailed information to appendices - focus on core 80% content")
                
        # Clarity recommendations
        if clarity_score < 70:
            recommendations.append("CLARITY: Improve readability - use shorter sentences and simpler language where possible")
            recommendations.append("CLARITY: Add more bullet points and lists to aid scanning and comprehension")
            
        # Context recommendations
        if context_score < 70:
            recommendations.append("CONTEXT: Strengthen context section - add project overview, technical stack, constraints, and key decisions")
            recommendations.append("CONTEXT: Move critical context to the beginning of the document")
            
        # Overall recommendations
        if not any('appendix' in s['title'].lower() for s in sections):
            recommendations.append("ORGANIZATION: Consider adding appendix sections for detailed reference material")
            
        if len(recommendations) == 0:
            recommendations.append("SUCCESS: Document quality is excellent! Consider periodic reviews to maintain effectiveness.")
            
        return recommendations
    
    def _calculate_metrics(self, content: str, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate detailed metrics for reporting"""
        total_words = len(content.split())
        
        return {
            'total_words': total_words,
            'total_sections': len(sections),
            'max_section_words': max((s['word_count'] for s in sections), default=0),
            'avg_section_words': round(sum(s['word_count'] for s in sections) / len(sections), 1) if sections else 0,
            'hierarchy_depth': max((s['level'] for s in sections), default=0),
            'has_code_blocks': '```' in content,
            'has_appendices': any('appendix' in s['title'].lower() for s in sections)
        }
