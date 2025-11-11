"""Wall entity - represents a wall segment in a blueprint."""

from dataclasses import dataclass
from typing import Optional

from ..value_objects.coordinates import Coordinates


@dataclass
class Wall:
    """
    Entity representing a wall segment in a blueprint.
    
    Attributes:
        id: Unique identifier for the wall
        start: Starting coordinates
        end: Ending coordinates
        thickness: Wall thickness in normalized units (default: 5)
        is_load_bearing: Whether the wall is load-bearing (default: False)
    """
    
    id: str
    start: Coordinates
    end: Coordinates
    thickness: float = 5.0
    is_load_bearing: bool = False
    
    def __post_init__(self):
        """Validate wall properties."""
        if self.thickness <= 0:
            raise ValueError(f"Wall thickness must be positive, got {self.thickness}")
        if self.thickness > 50:
            raise ValueError(f"Wall thickness seems too large: {self.thickness}")
    
    @property
    def length(self) -> float:
        """Calculate wall length."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return (dx ** 2 + dy ** 2) ** 0.5
    
    @property
    def is_horizontal(self) -> bool:
        """Check if wall is horizontal."""
        return abs(self.end.y - self.start.y) < 0.01
    
    @property
    def is_vertical(self) -> bool:
        """Check if wall is vertical."""
        return abs(self.end.x - self.start.x) < 0.01
    
    def to_dict(self) -> dict:
        """Convert wall to dictionary representation."""
        return {
            "id": self.id,
            "type": "line",
            "start": self.start.to_list(),
            "end": self.end.to_list(),
            "thickness": self.thickness,
            "is_load_bearing": self.is_load_bearing
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Wall":
        """Create Wall from dictionary representation."""
        return cls(
            id=data["id"],
            start=Coordinates(*data["start"]),
            end=Coordinates(*data["end"]),
            thickness=data.get("thickness", 5.0),
            is_load_bearing=data.get("is_load_bearing", False)
        )
    
    def __repr__(self) -> str:
        return f"Wall(id={self.id}, start={self.start}, end={self.end}, thickness={self.thickness})"

