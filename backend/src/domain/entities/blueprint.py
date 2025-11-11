"""Blueprint entity - represents a complete floor plan blueprint."""

from dataclasses import dataclass, field
from typing import List, Optional

from .room import Room
from .wall import Wall
from ..value_objects.coordinates import Coordinates


@dataclass
class Blueprint:
    """
    Entity representing a complete architectural blueprint.
    
    Attributes:
        id: Unique identifier for the blueprint
        width: Blueprint width in normalized units (default: 1000)
        height: Blueprint height in normalized units (default: 1000)
        walls: List of wall segments
        rooms: List of detected rooms (optional, may be empty initially)
        metadata: Additional metadata dictionary
    """
    
    id: str
    width: float = 1000.0
    height: float = 1000.0
    walls: List[Wall] = field(default_factory=list)
    rooms: List[Room] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate blueprint properties."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"Blueprint dimensions must be positive, got {self.width}x{self.height}")
        if self.width > 1000 or self.height > 1000:
            raise ValueError(f"Blueprint dimensions exceed normalized range, got {self.width}x{self.height}")
    
    def add_wall(self, wall: Wall) -> None:
        """Add a wall to the blueprint."""
        # Validate wall coordinates are within blueprint bounds
        if wall.start.x > self.width or wall.end.x > self.width:
            raise ValueError(f"Wall extends beyond blueprint width ({self.width})")
        if wall.start.y > self.height or wall.end.y > self.height:
            raise ValueError(f"Wall extends beyond blueprint height ({self.height})")
        self.walls.append(wall)
    
    def add_room(self, room: Room) -> None:
        """Add a room to the blueprint."""
        # Validate room bounding box is within blueprint bounds
        if room.bounding_box.x_max > self.width or room.bounding_box.y_max > self.height:
            raise ValueError(f"Room extends beyond blueprint bounds")
        self.rooms.append(room)
    
    def validate_layout(self) -> bool:
        """
        Validate that the blueprint layout is consistent.
        
        Returns:
            True if layout is valid, raises ValueError if invalid
        """
        if not self.walls:
            raise ValueError("Blueprint must have at least one wall")
        
        # Check for duplicate wall IDs
        wall_ids = [wall.id for wall in self.walls]
        if len(wall_ids) != len(set(wall_ids)):
            raise ValueError("Duplicate wall IDs found")
        
        # Check for duplicate room IDs
        if self.rooms:
            room_ids = [room.id for room in self.rooms]
            if len(room_ids) != len(set(room_ids)):
                raise ValueError("Duplicate room IDs found")
        
        return True
    
    def to_dict(self) -> dict:
        """Convert blueprint to dictionary representation."""
        return {
            "id": self.id,
            "width": self.width,
            "height": self.height,
            "walls": [wall.to_dict() for wall in self.walls],
            "rooms": [room.to_dict() for room in self.rooms],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Blueprint":
        """Create Blueprint from dictionary representation."""
        blueprint = cls(
            id=data["id"],
            width=data.get("width", 1000.0),
            height=data.get("height", 1000.0),
            metadata=data.get("metadata", {})
        )
        
        for wall_data in data.get("walls", []):
            blueprint.add_wall(Wall.from_dict(wall_data))
        
        for room_data in data.get("rooms", []):
            blueprint.add_room(Room.from_dict(room_data))
        
        return blueprint
    
    def __repr__(self) -> str:
        return f"Blueprint(id={self.id}, size={self.width}x{self.height}, walls={len(self.walls)}, rooms={len(self.rooms)})"

