"""Coordinates value object - represents a point in 2D space."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Coordinates:
    """
    Immutable value object representing 2D coordinates.
    
    Coordinates are normalized to 0-1000 range as per PRD requirements.
    """
    
    x: float
    y: float
    
    def __post_init__(self):
        """Validate coordinates are in valid range."""
        if not (0 <= self.x <= 1000):
            raise ValueError(f"X coordinate must be between 0 and 1000, got {self.x}")
        if not (0 <= self.y <= 1000):
            raise ValueError(f"Y coordinate must be between 0 and 1000, got {self.y}")
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple representation."""
        return (self.x, self.y)
    
    def to_list(self) -> list[float]:
        """Convert to list representation."""
        return [self.x, self.y]
    
    def __repr__(self) -> str:
        return f"Coordinates(x={self.x}, y={self.y})"

