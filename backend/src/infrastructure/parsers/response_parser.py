"""Parse and extract JSON from LLM responses."""

import json
import re
from typing import List, Dict, Optional


class ResponseParser:
    """Parses LLM responses to extract structured data."""
    
    @staticmethod
    def extract_json_from_response(response_text: str) -> str:
        """
        Extract JSON from LLM response text.
        
        Handles cases where JSON is wrapped in markdown code blocks.
        
        Args:
            response_text: Raw LLM response text
            
        Returns:
            JSON string
        """
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response_text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON array directly
        json_match = re.search(r'(\[.*?\])', response_text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # If no match, return original (might be pure JSON)
        return response_text.strip()
    
    @staticmethod
    def parse_room_data(json_str: str) -> List[Dict]:
        """
        Parse JSON string into list of room dictionaries.
        
        Args:
            json_str: JSON string containing room data
            
        Returns:
            List of room dictionaries
            
        Raises:
            ValueError: If JSON is invalid or malformed
        """
        try:
            data = json.loads(json_str)
            
            if not isinstance(data, list):
                raise ValueError("Expected JSON array, got other type")
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def sanitize_response(response_text: str) -> List[Dict]:
        """
        Complete pipeline: extract and parse JSON from response.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            List of room dictionaries
        """
        json_str = ResponseParser.extract_json_from_response(response_text)
        return ResponseParser.parse_room_data(json_str)

