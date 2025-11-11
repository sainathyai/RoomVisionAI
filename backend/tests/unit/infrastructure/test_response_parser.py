"""Unit tests for ResponseParser."""

import pytest

from backend.src.infrastructure.parsers.response_parser import ResponseParser


class TestResponseParser:
    """Test suite for ResponseParser."""
    
    def test_extract_json_from_markdown(self):
        """Test extracting JSON from markdown code block."""
        response = """Here's the result:
```json
[{"id": "room_001", "bounding_box": [100, 200, 500, 600]}]
```"""
        
        json_str = ResponseParser.extract_json_from_response(response)
        assert json_str.strip().startswith('[')
        assert "room_001" in json_str
    
    def test_extract_json_direct(self):
        """Test extracting JSON directly."""
        response = '[{"id": "room_001", "bounding_box": [100, 200, 500, 600]}]'
        
        json_str = ResponseParser.extract_json_from_response(response)
        assert json_str == response
    
    def test_parse_room_data_valid(self):
        """Test parsing valid room data."""
        json_str = '[{"id": "room_001", "bounding_box": [100, 200, 500, 600]}]'
        
        rooms = ResponseParser.parse_room_data(json_str)
        assert len(rooms) == 1
        assert rooms[0]["id"] == "room_001"
    
    def test_parse_room_data_invalid_json(self):
        """Test parsing fails for invalid JSON."""
        invalid_json = '[{"id": "room_001"}'  # Missing closing bracket
        
        with pytest.raises(ValueError):
            ResponseParser.parse_room_data(invalid_json)
    
    def test_parse_room_data_not_array(self):
        """Test parsing fails for non-array JSON."""
        not_array = '{"id": "room_001"}'
        
        with pytest.raises(ValueError, match="Expected JSON array"):
            ResponseParser.parse_room_data(not_array)
    
    def test_sanitize_response(self):
        """Test complete sanitization pipeline."""
        response = """Here's the result:
```json
[{"id": "room_001", "bounding_box": [100, 200, 500, 600]}]
```"""
        
        rooms = ResponseParser.sanitize_response(response)
        assert len(rooms) == 1
        assert rooms[0]["id"] == "room_001"

