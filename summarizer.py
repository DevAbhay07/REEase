import os
import json
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

class TextSummarizer:
    """Text summarization service using Google Gemini AI"""
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_summary(self, text: str, compression_ratio: Optional[str] = None) -> str:
        """Generate a summary of the provided text with optional compression ratio"""
        try:
            if not text or not text.strip():
                return "No content to summarize."
            
            # Build prompt based on compression ratio
            if compression_ratio == "25%":
                prompt = f"Summarize the following text to 25% of its original length. Keep only the most essential information:\n\n{text}"
            elif compression_ratio == "50%":
                prompt = f"Summarize the following text to 50% of its original length. Maintain key points and important details:\n\n{text}"
            elif compression_ratio == "75%":
                prompt = f"Summarize the following text to 75% of its original length. Preserve most details while making it more concise:\n\n{text}"
            else:
                prompt = f"Create a clear and concise summary of the following text, maintaining all important information:\n\n{text}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response and response.text:
                # Clean up the response text
                summary = response.text.strip()
                # Remove any asterisks or unwanted formatting
                summary = summary.replace('*', '').replace('#', '')
                return summary
            else:
                return "Failed to generate summary. Please try again."
                
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def summarize_json_threads(self, json_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Summarize JSON data containing email threads"""
        try:
            summaries = []
            
            # Group messages by thread_id
            thread_groups = {}
            for item in json_data:
                thread_id = item.get("thread_id")
                body = item.get("body", "")
                
                if thread_id is not None:
                    if thread_id not in thread_groups:
                        thread_groups[thread_id] = []
                    thread_groups[thread_id].append(body)
            
            # Generate summaries for each thread
            for thread_id, bodies in thread_groups.items():
                combined_text = " ".join(bodies).strip()
                
                if combined_text:
                    # Create a specific prompt for email thread summarization
                    prompt = f"Summarize this email thread in 60 words or less. Focus on key decisions, actions, and important details. Remove formatting characters and line breaks:\n\n{combined_text}"
                    
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt
                    )
                    
                    if response and response.text:
                        summary = response.text.strip()
                        # Clean up formatting
                        summary = summary.replace('*', '').replace('#', '').replace('\n', ' ')
                        summaries.append({
                            "thread_id": thread_id,
                            "body": summary
                        })
                    else:
                        summaries.append({
                            "thread_id": thread_id,
                            "body": "Failed to generate summary for this thread."
                        })
            
            return summaries
            
        except Exception as e:
            logging.error(f"Error summarizing JSON threads: {e}")
            return [{"error": f"Failed to process JSON data: {str(e)}"}]
