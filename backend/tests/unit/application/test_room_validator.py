"""Unit tests for RoomValidator."""

import pytest

from backend.src.application.validators.room_validator import RoomValidator


class TestRoomValidator:
    """Test suite for RoomValidator."""
    
    def test_validate_room_valid(self):
        """Test validation of valid room."""
        room = {
            "id": "room_001",
            "bounding_box": [100, 200, 500, 600],
            "name_hint": "Kitchen"
        }
        
        assert RoomValidator.validate_room(room) is True
    
    def test_validate_room_missing_id(self):
        """Test validation fails for missing id."""
        room = {"bounding_box": [100, 200, 500, 600]}
        
        with pytest.raises(ValueError, match="missing 'id' field"):
            RoomValidator.validate_room(room)
    
    def test_validate_room_missing_bbox(self):
        """Test validation fails for missing bounding_box."""
        room = {"id": "room_001"}
        
        with pytest.raises(ValueError, match="missing 'bounding_box' field"):
            RoomValidator.validate_room(room)
    
    def test_validate_bounding_box_valid(self):
        """Test validation of valid bounding box."""
        bbox = [100, 200, 500, 600]
        assert RoomValidator.validate_bounding_box(bbox) is True
    
    def test_validate_bounding_box_invalid_range(self):
        """Test validation fails for out-of-range coordinates."""
        bbox = [100, 200, 1500, 600]  # x_max > 1000
        
        with pytest.raises(ValueError, match="must be between"):
            RoomValidator.validate_bounding_box(bbox)
    
    def test_validate_bounding_box_invalid_geometry(self):
        """Test validation fails for invalid box geometry."""
        bbox = [500, 200, 100, 600]  # x_min > x_max
        
        with pytest.raises(ValueError, match="must be less than"):
            RoomValidator.validate_bounding_box(bbox)
    
    def test_validate_rooms_filters_invalid(self):
        """Test validate_rooms filters out invalid rooms."""
        rooms = [
            {"id": "room_001", "bounding_box": [100, 200, 500, 600]},  # Valid
            {"id": "room_002", "bounding_box": [500, 200, 100, 600]},  # Invalid (x_min > x_max)
            {"id": "room_003", "bounding_box": [200, 300, 600, 700]}   # Valid
        ]
        
        valid_rooms = RoomValidator.validate_rooms(rooms)
        assert len(valid_rooms) == 2
        assert valid_rooms[0]["id"] == "room_001"
        assert valid_rooms[1]["id"] == "room_003"
    
    def test_sanitize_coordinates(self):
        """Test coordinate sanitization."""
        bbox = [-10, 200, 1500, 600]  # Out of range
        sanitized = RoomValidator.sanitize_coordinates(bbox)
        
        assert sanitized[0] >= 0  # x_min clamped
        assert sanitized[2] <= 1000  # x_max clamped
        assert sanitized[0] < sanitized[2]  # Valid geometry

