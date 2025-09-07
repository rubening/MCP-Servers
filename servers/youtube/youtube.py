#!/usr/bin/env python3
"""
YouTube MCP Server
==================

Model Context Protocol server for YouTube transcript extraction and checklist generation.
Integrates the robust YouTube transcript to checklist converter into Claude's MCP system.

Features:
- Primary: youtube-transcript-api (fast)
- Fallback: yt-dlp (robust, handles format changes)
- Complete automation with zero manual steps
- Direct integration with Claude tools

Author: Enhanced for Ruben - MCP Integration Version
Version: 1.0.0 - ROBUST MCP SERVER
Protocol: JSON-RPC 2.0 compatible (2024-11-05)
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Setup logging
log_file = r"C:\Users\ruben\Claude Tools\logs\youtube_mcp.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def install_dependencies():
    """Install required dependencies including yt-dlp fallback."""
    required_packages = ['youtube-transcript-api', 'yt-dlp']
    
    for package in required_packages:
        try:
            if package == 'youtube-transcript-api':
                __import__('youtube_transcript_api')
            elif package == 'yt-dlp':
                __import__('yt_dlp')
        except ImportError:
            logger.info(f"Installing {package}...")
            try:
                # Redirect stdout and stderr to prevent interfering with JSON-RPC
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.info(f"{package} installed successfully!")
            except Exception as e:
                logger.warning(f"Could not install {package}: {e}")

def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    url = url.strip()
    
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    
    return None

def get_transcript_primary_method(video_id: str) -> Tuple[Optional[str], Optional[Dict], str]:
    """
    Primary method: Use youtube-transcript-api (faster when it works).
    Returns: (transcript_text, transcript_data, method_used)
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
        
        logger.info("Trying youtube-transcript-api...")
        
        # Get transcript list
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get English transcript (manual first, then auto-generated)
        transcript = None
        
        # Try manually created English
        try:
            transcript = transcript_list.find_transcript(['en'])
            logger.info("Found manually created English transcript")
        except:
            pass
        
        # Try auto-generated English
        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
                logger.info("Found auto-generated English transcript")
            except:
                pass
        
        # Try any available transcript
        if transcript is None:
            for available_transcript in transcript_list:
                transcript = available_transcript
                logger.info(f"Using {available_transcript.language} transcript")
                break
        
        if transcript is None:
            logger.info("No transcripts found")
            return None, None, "primary_failed_no_transcripts"
        
        # Fetch and format
        transcript_data = transcript.fetch()
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript_data)
        
        logger.info(f"SUCCESS! Extracted {len(transcript_text)} characters")
        return transcript_text, transcript_data, "youtube-transcript-api"
        
    except Exception as e:
        error_str = str(e)
        logger.info(f"Primary method failed: {error_str}")
        
        if "no element found" in error_str:
            logger.info("Detected XML parsing error - this is the known issue")
        
        return None, None, f"primary_failed_{type(e).__name__}"

def get_transcript_fallback_method(video_id: str) -> Tuple[Optional[str], Optional[Dict], str]:
    """
    Fallback method: Use yt-dlp (more robust, handles YouTube changes).
    Returns: (transcript_text, transcript_data, method_used)
    """
    try:
        logger.info("Trying yt-dlp method...")
        
        # Try to import yt-dlp
        try:
            import yt_dlp
        except ImportError:
            logger.info("yt-dlp not available")
            return None, None, "fallback_failed_no_ytdlp"
        
        # Setup yt-dlp options
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
            'no_color': True,
            'extractor_args': {'youtube': {'player_client': ['android']}},
        }
        
        # Create temporary directory for subtitle files
        temp_dir = os.path.join(os.getcwd(), 'temp_subs')
        os.makedirs(temp_dir, exist_ok=True)
        ydl_opts['outtmpl'] = os.path.join(temp_dir, f'{video_id}.%(ext)s')
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                logger.info("Downloading subtitles with yt-dlp...")
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
            except Exception as e:
                logger.info(f"yt-dlp download failed: {str(e)}")
                return None, None, f"fallback_failed_download_{type(e).__name__}"
        
        # Look for subtitle files
        subtitle_files = []
        for file in os.listdir(temp_dir):
            if file.startswith(video_id) and file.endswith('.vtt'):
                subtitle_files.append(os.path.join(temp_dir, file))
        
        if not subtitle_files:
            logger.info("No subtitle files found")
            # Cleanup
            try:
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file))
                os.rmdir(temp_dir)
            except:
                pass
            return None, None, "fallback_failed_no_subtitle_files"
        
        # Read the first subtitle file
        subtitle_file = subtitle_files[0]
        logger.info(f"Reading subtitle file: {os.path.basename(subtitle_file)}")
        
        try:
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                vtt_content = f.read()
        except Exception as e:
            logger.info(f"Could not read subtitle file: {str(e)}")
            return None, None, f"fallback_failed_read_{type(e).__name__}"
        
        # Parse VTT content
        transcript_text = parse_vtt_content(vtt_content)
        
        if not transcript_text:
            logger.info("Could not parse VTT content")
            return None, None, "fallback_failed_parse_vtt"
        
        # Create transcript data (simplified format)
        transcript_data = [{"text": transcript_text, "start": 0.0}]
        
        # Cleanup temp files
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
        
        logger.info(f"SUCCESS! Extracted {len(transcript_text)} characters using yt-dlp")
        return transcript_text, transcript_data, "yt-dlp"
        
    except Exception as e:
        logger.info(f"Fallback method unexpected error: {str(e)}")
        return None, None, f"fallback_failed_unexpected_{type(e).__name__}"

def parse_vtt_content(vtt_content: str) -> Optional[str]:
    """Parse VTT (WebVTT) subtitle content and extract text."""
    lines = vtt_content.split('\n')
    text_parts = []
    
    for line in lines:
        line = line.strip()
        
        # Skip VTT headers, timestamps, and empty lines
        if (line.startswith('WEBVTT') or 
            line.startswith('NOTE') or
            '-->' in line or
            line.isdigit() or
            not line):
            continue
        
        # Remove VTT styling tags
        line = re.sub(r'<[^>]+>', '', line)
        
        if line:
            text_parts.append(line)
    
    return ' '.join(text_parts) if text_parts else None

def get_transcript_robust(video_id: str) -> Tuple[Optional[str], Optional[Dict], str]:
    """
    Robust transcript extraction with primary method + fallback.
    Returns: (transcript_text, transcript_data, method_used)
    """
    logger.info(f"Starting robust transcript extraction for {video_id}")
    
    # Try primary method first
    transcript_text, transcript_data, method = get_transcript_primary_method(video_id)
    
    if transcript_text:
        return transcript_text, transcript_data, method
    
    logger.info("Primary method failed, trying fallback...")
    
    # Try fallback method
    transcript_text, transcript_data, method = get_transcript_fallback_method(video_id)
    
    if transcript_text:
        return transcript_text, transcript_data, method
    
    logger.info("All methods failed")
    return None, None, "all_methods_failed"

def get_video_info(video_id: str) -> Dict[str, str]:
    """Get basic video information."""
    return {
        'video_id': video_id,
        'title': f"YouTube Video {video_id}",
        'url': f"https://www.youtube.com/watch?v={video_id}"
    }

def generate_checklist_ai(transcript: str, video_info: Dict[str, str]) -> str:
    """Generate checklist using AI processing."""
    
    logger.info("Starting intelligent checklist generation...")
    
    # Truncate transcript if too long
    if len(transcript) > 15000:
        logger.info(f"Transcript is {len(transcript)} characters - using first 15000 for analysis")
        working_transcript = transcript[:15000] + "\n\n[Note: Transcript truncated for processing]"
    else:
        working_transcript = transcript
    
    # Analyze content type
    has_instructions = any(keyword in transcript.lower() for keyword in [
        'how to', 'step', 'first', 'next', 'then', 'now', 'let\'s', 'you need to',
        'make sure', 'important', 'remember', 'tutorial', 'guide', 'process',
        'install', 'setup', 'configure', 'build', 'create', 'add', 'remove'
    ])
    
    if has_instructions:
        logger.info("Detected instructional content - generating step-by-step checklist")
        checklist_type = "instructional"
    else:
        logger.info("Detected review/commentary content - generating key points checklist")
        checklist_type = "review"
    
    # Split into segments
    lines = working_transcript.split('\n')
    text_segments = []
    current_segment = ""
    
    for line in lines:
        line = line.strip()
        if line:
            current_segment += line + " "
            if (line.endswith('.') or line.endswith('!') or line.endswith('?') or 
                len(current_segment) > 200) and len(current_segment) > 50:
                text_segments.append(current_segment.strip())
                current_segment = ""
    
    if current_segment.strip():
        text_segments.append(current_segment.strip())
    
    logger.info(f"Identified {len(text_segments)} content segments for analysis")
    
    # Generate checklist
    if checklist_type == "instructional":
        checklist = generate_instructional_checklist(text_segments, video_info)
    else:
        checklist = generate_review_checklist(text_segments, video_info, transcript)
    
    logger.info("Checklist generation complete!")
    return checklist

def generate_instructional_checklist(segments: List[str], video_info: Dict[str, str]) -> str:
    """Generate checklist for instructional content."""
    
    action_keywords = ['install', 'download', 'create', 'open', 'click', 'add', 'remove', 
                      'setup', 'configure', 'build', 'run', 'execute', 'make', 'set',
                      'copy', 'paste', 'save', 'delete', 'move', 'edit', 'change']
    
    checklist_items = []
    
    for segment in segments:
        segment_lower = segment.lower()
        
        if any(keyword in segment_lower for keyword in action_keywords):
            sentences = segment.split('. ')
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in action_keywords):
                    if sentence and not sentence.endswith('.'):
                        sentence += '.'
                    
                    sentence = re.sub(r'\b(um|uh|you know|like|basically|actually)\b', '', sentence, flags=re.IGNORECASE)
                    sentence = ' '.join(sentence.split())
                    
                    if len(sentence) > 20 and len(sentence) < 300:
                        if not sentence.lower().startswith(('install', 'download', 'create', 'open', 'click')):
                            sentence = "**" + sentence.split()[0].title() + "** " + ' '.join(sentence.split()[1:])
                        else:
                            sentence = "**" + sentence.split()[0].title() + "** " + ' '.join(sentence.split()[1:])
                        
                        checklist_items.append(f"- [ ] {sentence}")
    
    if len(checklist_items) < 3:
        checklist_items = extract_key_points(segments)
    
    checklist = f"""# YouTube Video Checklist

**Source:** {video_info['url']}
**Video ID:** {video_info['video_id']}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Steps to Follow

"""
    
    seen = set()
    for item in checklist_items[:15]:
        if item not in seen:
            checklist += item + "\n"
            seen.add(item)
    
    if not checklist_items:
        checklist += "- [ ] **Watch the video** for specific instructions\n"
        checklist += "- [ ] **Take notes** on key points mentioned\n"
        checklist += "- [ ] **Follow along** with the demonstration\n"
    
    return checklist

def generate_review_checklist(segments: List[str], video_info: Dict[str, str], full_transcript: str) -> str:
    """Generate checklist for review/commentary content."""
    
    key_points = []
    positive_words = ['good', 'great', 'awesome', 'excellent', 'love', 'like', 'impressed', 'solid']
    negative_words = ['bad', 'terrible', 'hate', 'disappointing', 'issues', 'problems', 'buggy']
    feature_words = ['feature', 'system', 'mechanic', 'graphics', 'sound', 'gameplay', 'story']
    
    for segment in segments:
        segment_lower = segment.lower()
        
        if any(word in segment_lower for word in positive_words + negative_words + feature_words):
            sentences = segment.split('. ')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 30 and len(sentence) < 200:
                    sentence = re.sub(r'\b(um|uh|you know|like|basically|actually)\b', '', sentence, flags=re.IGNORECASE)
                    sentence = ' '.join(sentence.split())
                    
                    if sentence:
                        key_points.append(sentence)
    
    checklist = f"""# YouTube Video Review Checklist

**Source:** {video_info['url']}
**Video ID:** {video_info['video_id']}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Points to Consider

"""
    
    seen_topics = set()
    for point in key_points[:12]:
        words = point.lower().split()
        topic_word = None
        for word in words:
            if word in ['game', 'graphics', 'sound', 'story', 'gameplay', 'combat', 'building', 'features']:
                topic_word = word
                break
        
        if topic_word and topic_word not in seen_topics:
            checklist += f"- [ ] **Evaluate {topic_word}** - {point}\n"
            seen_topics.add(topic_word)
        elif not topic_word:
            checklist += f"- [ ] **Consider** - {point}\n"
    
    if len(key_points) < 5:
        checklist += "- [ ] **Note the reviewer's overall opinion** of the subject\n"
        checklist += "- [ ] **Identify key strengths** mentioned in the review\n"
        checklist += "- [ ] **Identify key weaknesses** mentioned in the review\n"
        checklist += "- [ ] **Consider the reviewer's background** and expertise\n"
        checklist += "- [ ] **Evaluate relevance** to your own interests or needs\n"
    
    return checklist

def extract_key_points(segments: List[str]) -> List[str]:
    """Extract key points when specific instructions aren't found."""
    
    points = []
    important_indicators = ['important', 'key', 'main', 'essential', 'critical', 'remember', 'note']
    
    for segment in segments:
        segment_lower = segment.lower()
        
        if (any(indicator in segment_lower for indicator in important_indicators) or
            segment.endswith('!') or 'you should' in segment_lower or 'make sure' in segment_lower):
            
            clean_segment = re.sub(r'\b(um|uh|you know|like|basically|actually)\b', '', segment, flags=re.IGNORECASE)
            clean_segment = ' '.join(clean_segment.split())
            
            if len(clean_segment) > 20 and len(clean_segment) < 250:
                points.append(f"- [ ] **Remember** - {clean_segment}")
    
    return points

def save_results(video_info: Dict[str, str], transcript: str, transcript_data: List[Dict], 
                checklist: str, method_used: str) -> Dict[str, str]:
    """Save all results with method information."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_video_id = re.sub(r'[^\w\-_]', '_', video_info['video_id'])
    
    base_path = "C:\\Users\\ruben\\Claude Tools\\projects\\ai-tools\\youtube-checklister\\outputs"
    
    try:
        os.makedirs(base_path, exist_ok=True)
    except:
        base_path = "."
    
    files_created = {}
    
    # Save transcript
    transcript_file = os.path.join(base_path, f"{safe_video_id}_{timestamp}_transcript.txt")
    try:
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"YouTube Video Transcript\n")
            f.write(f"========================\n\n")
            f.write(f"Video ID: {video_info['video_id']}\n")
            f.write(f"Title: {video_info.get('title', 'Unknown')}\n")
            f.write(f"URL: {video_info['url']}\n")
            f.write(f"Extraction Method: {method_used}\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("TRANSCRIPT:\n")
            f.write("=" * 50 + "\n\n")
            f.write(transcript)
        files_created['transcript'] = transcript_file
    except Exception as e:
        logger.warning(f"Could not save transcript: {e}")
    
    # Save JSON data
    json_file = os.path.join(base_path, f"{safe_video_id}_{timestamp}_raw_data.json")
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'video_info': video_info,
                'transcript_data': transcript_data,
                'extraction_method': method_used,
                'processed_at': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        files_created['json'] = json_file
    except Exception as e:
        logger.warning(f"Could not save JSON data: {e}")
    
    # Save checklist
    checklist_file = os.path.join(base_path, f"{safe_video_id}_{timestamp}_CHECKLIST.md")
    try:
        # Add method information to checklist
        enhanced_checklist = f"*Transcript extracted using: {method_used}*\n\n" + checklist
        
        with open(checklist_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_checklist)
        files_created['checklist'] = checklist_file
        logger.info(f"AUTO-GENERATED CHECKLIST saved: {checklist_file}")
    except Exception as e:
        logger.warning(f"Could not save checklist: {e}")
    
    return files_created

# MCP Server Implementation
class YouTubeMCPServer:
    def __init__(self):
        self.server_info = {
            "name": "youtube-mcp",
            "version": "1.0.0"
        }
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        logger.info("Initializing YouTube MCP Server")
        
        # Install dependencies on initialization
        install_dependencies()
        
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        }
    
    async def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available YouTube tools"""
        tools = [
            {
                "name": "youtube_to_checklist",
                "description": "Convert YouTube video to actionable checklist with robust transcript extraction",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "YouTube URL or video ID"
                        },
                        "save_files": {
                            "type": "boolean",
                            "description": "Whether to save transcript and checklist files (default: true)",
                            "default": True
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "youtube_transcript",
                "description": "Extract only the transcript from YouTube video with robust fallback methods",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "YouTube URL or video ID"
                        },
                        "save_file": {
                            "type": "boolean",
                            "description": "Whether to save transcript file (default: false)",
                            "default": False
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "youtube_debug",
                "description": "Debug YouTube transcript extraction issues and show detailed information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "YouTube URL or video ID"
                        }
                    },
                    "required": ["url"]
                }
            }
        ]
        
        return {"tools": tools}
    
    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "youtube_to_checklist":
                return await self.youtube_to_checklist(arguments)
            elif tool_name == "youtube_transcript":
                return await self.youtube_transcript(arguments)
            elif tool_name == "youtube_debug":
                return await self.youtube_debug(arguments)
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Unknown tool: {tool_name}"
                        }
                    ],
                    "isError": True
                }
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing {tool_name}: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    async def youtube_to_checklist(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Convert YouTube video to checklist"""
        url = arguments.get("url")
        save_files = arguments.get("save_files", True)
        
        logger.info(f"Converting YouTube video to checklist: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "ERROR: Invalid YouTube URL format. Please provide a valid YouTube URL or video ID."
                    }
                ],
                "isError": True
            }
        
        # Get video info
        video_info = get_video_info(video_id)
        
        # Extract transcript with robust method
        transcript_text, transcript_data, method_used = get_transcript_robust(video_id)
        
        if not transcript_text:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"""ERROR: Transcript Extraction Failed

Could not extract transcript for video ID: {video_id}

Possible reasons:
- Video has no subtitles/captions available
- Video is private or restricted
- Video has regional restrictions
- Unusual transcript formatting

Try: A different video or check if the video has captions enabled."""
                    }
                ],
                "isError": True
            }
        
        # Generate checklist
        checklist = generate_checklist_ai(transcript_text, video_info)
        
        # Save files if requested
        files_created = {}
        if save_files:
            files_created = save_results(video_info, transcript_text, transcript_data, checklist, method_used)
        
        # Prepare response
        response_text = f"""SUCCESS: YouTube Video Successfully Converted to Checklist

Video ID: {video_id}
URL: {video_info['url']}
Extraction Method: {method_used}
Transcript Length: {len(transcript_text)} characters

---

{checklist}

---

"""
        
        if save_files and files_created:
            response_text += "Files Created:\n"
            for file_type, file_path in files_created.items():
                response_text += f"- {file_type.title()}: {file_path}\n"
        else:
            response_text += "Files not saved (save_files=false)"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        }
    
    async def youtube_transcript(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Extract only transcript from YouTube video"""
        url = arguments.get("url")
        save_file = arguments.get("save_file", False)
        
        logger.info(f"Extracting transcript from YouTube video: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "ERROR: Invalid YouTube URL format. Please provide a valid YouTube URL or video ID."
                    }
                ],
                "isError": True
            }
        
        # Get video info
        video_info = get_video_info(video_id)
        
        # Extract transcript with robust method
        transcript_text, transcript_data, method_used = get_transcript_robust(video_id)
        
        if not transcript_text:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"""ERROR: Transcript Extraction Failed

Could not extract transcript for video ID: {video_id}

Possible reasons:
- Video has no subtitles/captions available
- Video is private or restricted
- Video has regional restrictions
- Unusual transcript formatting"""
                    }
                ],
                "isError": True
            }
        
        # Save file if requested
        file_created = None
        if save_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_video_id = re.sub(r'[^\w\-_]', '_', video_info['video_id'])
            base_path = "C:\\Users\\ruben\\Claude Tools\\projects\\ai-tools\\youtube-checklister\\outputs"
            
            try:
                os.makedirs(base_path, exist_ok=True)
                transcript_file = os.path.join(base_path, f"{safe_video_id}_{timestamp}_transcript.txt")
                
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(f"YouTube Video Transcript\n")
                    f.write(f"========================\n\n")
                    f.write(f"Video ID: {video_info['video_id']}\n")
                    f.write(f"URL: {video_info['url']}\n")
                    f.write(f"Extraction Method: {method_used}\n")
                    f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("TRANSCRIPT:\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(transcript_text)
                
                file_created = transcript_file
            except Exception as e:
                logger.warning(f"Could not save transcript file: {e}")
        
        # Prepare response
        response_text = f"""SUCCESS: Transcript Successfully Extracted

Video ID: {video_id}
URL: {video_info['url']}
Extraction Method: {method_used}
Length: {len(transcript_text)} characters

---

TRANSCRIPT:

{transcript_text[:2000]}{"..." if len(transcript_text) > 2000 else ""}

---

"""
        
        if file_created:
            response_text += f"File Created: {file_created}"
        else:
            response_text += "File not saved"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        }
    
    async def youtube_debug(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Debug YouTube transcript extraction"""
        url = arguments.get("url")
        
        logger.info(f"Debugging YouTube transcript extraction: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "ERROR: Invalid YouTube URL format. Please provide a valid YouTube URL or video ID."
                    }
                ],
                "isError": True
            }
        
        debug_info = []
        debug_info.append(f"YouTube Transcript Debug Information\n")
        debug_info.append(f"Video ID: {video_id}")
        debug_info.append(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        
        # Test primary method
        debug_info.append("Testing Primary Method (youtube-transcript-api):")
        transcript_text, transcript_data, method = get_transcript_primary_method(video_id)
        
        if transcript_text:
            debug_info.append(f"SUCCESS - Extracted {len(transcript_text)} characters")
            debug_info.append(f"Method: {method}")
        else:
            debug_info.append(f"FAILED - {method}")
        
        debug_info.append("")
        
        # Test fallback method if primary failed
        if not transcript_text:
            debug_info.append("Testing Fallback Method (yt-dlp):")
            transcript_text, transcript_data, method = get_transcript_fallback_method(video_id)
            
            if transcript_text:
                debug_info.append(f"SUCCESS - Extracted {len(transcript_text)} characters")
                debug_info.append(f"Method: {method}")
            else:
                debug_info.append(f"FAILED - {method}")
        
        debug_info.append("")
        
        # Final status
        if transcript_text:
            debug_info.append("Overall Result: SUCCESS")
            debug_info.append(f"Final Method: {method}")
            debug_info.append(f"Transcript Preview: {transcript_text[:500]}...")
        else:
            debug_info.append("Overall Result: FAILED")
            debug_info.append("Recommendation: Try a different video or verify the video has captions")
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": "\n".join(debug_info)
                }
            ]
        }

async def main():
    """Main MCP server loop"""
    server = YouTubeMCPServer()
    
    logger.info("Starting YouTube MCP Server...")
    
    while True:
        try:
            # Use async stdin reading for compatibility with Claude Desktop
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON received: {e}")
                continue
            
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            # Handle different MCP methods
            if method == "initialize":
                result = await server.handle_initialize(params)
            elif method == "tools/list":
                result = await server.handle_list_tools(params)
            elif method == "tools/call":
                result = await server.handle_call_tool(params)
            else:
                logger.warning(f"Unknown method: {method}")
                continue
            
            # Send response
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            if 'request_id' in locals():
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())

