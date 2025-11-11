"""Unit tests for Room entity."""

from backend.src.domain.entities.room import Room
from backend.src.domain.value_objects.bounding_box import BoundingBox


class TestRoom:
    """Test suite for Room entity."""
    
    def test_create_room_without_name(self):
        """Test creating a room without a name."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        room = Room(id="room_001", bounding_box=bbox)
        
        assert room.id == "room_001"
        assert room.bounding_box == bbox
        assert room.name_hint is None
    
    def test_create_room_with_name(self):
        """Test creating a room with a name."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        room = Room(id="room_001", bounding_box=bbox, name_hint="Kitchen")
        
        assert room.id == "room_001"
        assert room.bounding_box == bbox
        assert room.name_hint == "Kitchen"
    
    def test_room_area(self):
        """Test room area calculation."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        room = Room(id="room_001", bounding_box=bbox)
        
        assert room.area == 160000  # 400 * 400
    
    def test_room_to_dict_without_name(self):
        """Test converting room to dict without name."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        room = Room(id="room_001", bounding_box=bbox)
        
        result = room.to_dict()
        assert result == {
            "id": "room_001",
            "bounding_box": [100, 200, 500, 600]
        }
    
    def test_room_to_dict_with_name(self):
        """Test converting room to dict with name."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        room = Room(id="room_001", bounding_box=bbox, name_hint="Kitchen")
        
        result = room.to_dict()
        assert result == {
            "id": "room_001",
            "bounding_box": [100, 200, 500, 600],
            "name_hint": "Kitchen"
        }
    
    def test_room_from_dict_without_name(self):
        """Test creating room from dict without name."""
        data = {
            "id": "room_001",
            "bounding_box": [100, 200, 500, 600]
        }
        room = Room.from_dict(data)
        
        assert room.id == "room_001"
        assert room.bounding_box.x_min == 100
        assert room.name_hint is None
    
    def test_room_from_dict_with_name(self):
        """Test creating room from dict with name."""
        data = {
            "id": "room_001",
            "bounding_box": [100, 200, 500, 600],
            "name_hint": "Kitchen"
        }
        room = Room.from_dict(data)
        
        assert room.id == "room_001"
        assert room.bounding_box.x_min == 100
        assert room.name_hint == "Kitchen"

