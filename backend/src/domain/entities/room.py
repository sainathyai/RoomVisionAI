"""Room entity - represents a room in a blueprint."""

from dataclasses import dataclass
from typing import Optional

from ..value_objects.bounding_box import BoundingBox


@dataclass
class Room:
    """
    Entity representing a room in a blueprint.
    
    Attributes:
        id: Unique identifier for the room
        bounding_box: Bounding box coordinates [x_min, y_min, x_max, y_max]
        name_hint: Optional room name or type (e.g., "Kitchen", "Office")
    """
    
    id: str
    bounding_box: BoundingBox
    name_hint: Optional[str] = None
    
    @property
    def area(self) -> float:
        """Calculate room area."""
        return self.bounding_box.area
    
    def to_dict(self) -> dict:
        """Convert room to dictionary representation matching PRD schema."""
        result = {
            "id": self.id,
            "bounding_box": self.bounding_box.to_list()
        }
        if self.name_hint:
            result["name_hint"] = self.name_hint
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        """Create Room from dictionary representation."""
        return cls(
            id=data["id"],
            bounding_box=BoundingBox.from_list(data["bounding_box"]),
            name_hint=data.get("name_hint")
        )
    
    def __repr__(self) -> str:
        name = f", name={self.name_hint}" if self.name_hint else ""
        return f"Room(id={self.id}{name}, bbox={self.bounding_box})"

