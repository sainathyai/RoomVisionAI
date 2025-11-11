"""Validate detected room data."""

from typing import List, Dict, Optional


class RoomValidator:
    """Validates room detection results."""
    
    COORDINATE_MIN = 0
    COORDINATE_MAX = 1000
    
    @staticmethod
    def validate_room(room: Dict) -> bool:
        """
        Validate a single room dictionary.
        
        Args:
            room: Room dictionary with id and bounding_box
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        # Check required fields
        if "id" not in room:
            raise ValueError("Room missing 'id' field")
        
        if "bounding_box" not in room:
            raise ValueError(f"Room {room.get('id', 'unknown')} missing 'bounding_box' field")
        
        # Validate bounding box
        bbox = room["bounding_box"]
        RoomValidator.validate_bounding_box(bbox, room["id"])
        
        return True
    
    @staticmethod
    def validate_bounding_box(bbox: List[float], room_id: Optional[str] = None) -> bool:
        """
        Validate bounding box coordinates.
        
        Args:
            bbox: Bounding box [x_min, y_min, x_max, y_max]
            room_id: Optional room ID for error messages
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        if not isinstance(bbox, list):
            raise ValueError(f"Bounding box must be a list, got {type(bbox)}")
        
        if len(bbox) != 4:
            raise ValueError(f"Bounding box must have 4 coordinates, got {len(bbox)}")
        
        x_min, y_min, x_max, y_max = bbox
        
        # Validate coordinate range
        for coord, name in [(x_min, "x_min"), (y_min, "y_min"), (x_max, "x_max"), (y_max, "y_max")]:
            if not isinstance(coord, (int, float)):
                raise ValueError(f"{name} must be a number, got {type(coord)}")
            
            if not (RoomValidator.COORDINATE_MIN <= coord <= RoomValidator.COORDINATE_MAX):
                raise ValueError(
                    f"{name} ({coord}) must be between {RoomValidator.COORDINATE_MIN} "
                    f"and {RoomValidator.COORDINATE_MAX}"
                )
        
        # Validate box geometry
        if x_min >= x_max:
            raise ValueError(f"x_min ({x_min}) must be less than x_max ({x_max})")
        
        if y_min >= y_max:
            raise ValueError(f"y_min ({y_min}) must be less than y_max ({y_max})")
        
        return True
    
    @staticmethod
    def validate_rooms(rooms: List[Dict]) -> List[Dict]:
        """
        Validate list of rooms, filtering out invalid ones.
        
        Args:
            rooms: List of room dictionaries
            
        Returns:
            List of valid room dictionaries
        """
        valid_rooms = []
        
        for room in rooms:
            try:
                RoomValidator.validate_room(room)
                valid_rooms.append(room)
            except ValueError as e:
                # Log error but continue processing
                print(f"Warning: Invalid room filtered out: {e}")
                continue
        
        return valid_rooms
    
    @staticmethod
    def sanitize_coordinates(bbox: List[float]) -> List[float]:
        """
        Sanitize coordinates by clamping to valid range.
        
        Args:
            bbox: Bounding box coordinates
            
        Returns:
            Sanitized bounding box
        """
        x_min, y_min, x_max, y_max = bbox
        
        x_min = max(RoomValidator.COORDINATE_MIN, min(x_min, RoomValidator.COORDINATE_MAX))
        y_min = max(RoomValidator.COORDINATE_MIN, min(y_min, RoomValidator.COORDINATE_MAX))
        x_max = max(RoomValidator.COORDINATE_MIN, min(x_max, RoomValidator.COORDINATE_MAX))
        y_max = max(RoomValidator.COORDINATE_MIN, min(y_max, RoomValidator.COORDINATE_MAX))
        
        # Ensure min < max
        if x_min >= x_max:
            x_max = min(x_min + 1, RoomValidator.COORDINATE_MAX)
        if y_min >= y_max:
            y_max = min(y_min + 1, RoomValidator.COORDINATE_MAX)
        
        return [x_min, y_min, x_max, y_max]

