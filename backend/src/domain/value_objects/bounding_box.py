"""BoundingBox value object - represents a rectangular area."""

from dataclasses import dataclass
from typing import List

from .coordinates import Coordinates


@dataclass(frozen=True)
class BoundingBox:
    """
    Immutable value object representing a rectangular bounding box.
    
    Format: [x_min, y_min, x_max, y_max] normalized to 0-1000 range.
    """
    
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    
    def __post_init__(self):
        """Validate bounding box coordinates."""
        if not (0 <= self.x_min <= 1000):
            raise ValueError(f"x_min must be between 0 and 1000, got {self.x_min}")
        if not (0 <= self.y_min <= 1000):
            raise ValueError(f"y_min must be between 0 and 1000, got {self.y_min}")
        if not (0 <= self.x_max <= 1000):
            raise ValueError(f"x_max must be between 0 and 1000, got {self.x_max}")
        if not (0 <= self.y_max <= 1000):
            raise ValueError(f"y_max must be between 0 and 1000, got {self.y_max}")
        if self.x_min >= self.x_max:
            raise ValueError(f"x_min ({self.x_min}) must be less than x_max ({self.x_max})")
        if self.y_min >= self.y_max:
            raise ValueError(f"y_min ({self.y_min}) must be less than y_max ({self.y_max})")
    
    @property
    def width(self) -> float:
        """Calculate width of the bounding box."""
        return self.x_max - self.x_min
    
    @property
    def height(self) -> float:
        """Calculate height of the bounding box."""
        return self.y_max - self.y_min
    
    @property
    def area(self) -> float:
        """Calculate area of the bounding box."""
        return self.width * self.height
    
    @property
    def center(self) -> Coordinates:
        """Get center point of the bounding box."""
        return Coordinates(
            x=(self.x_min + self.x_max) / 2,
            y=(self.y_min + self.y_max) / 2
        )
    
    def to_list(self) -> List[float]:
        """Convert to list representation [x_min, y_min, x_max, y_max]."""
        return [self.x_min, self.y_min, self.x_max, self.y_max]
    
    @classmethod
    def from_list(cls, coords: List[float]) -> "BoundingBox":
        """Create BoundingBox from list [x_min, y_min, x_max, y_max]."""
        if len(coords) != 4:
            raise ValueError(f"Expected 4 coordinates, got {len(coords)}")
        return cls(
            x_min=coords[0],
            y_min=coords[1],
            x_max=coords[2],
            y_max=coords[3]
        )
    
    def contains(self, point: Coordinates) -> bool:
        """Check if point is inside the bounding box."""
        return (
            self.x_min <= point.x <= self.x_max and
            self.y_min <= point.y <= self.y_max
        )
    
    def __repr__(self) -> str:
        return f"BoundingBox(x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max})"

