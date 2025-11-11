"""
Blueprint Generator - Main script for generating synthetic blueprints.

This script provides a high-level interface for creating floor plans
and generating blueprint images using Clean Architecture.
"""

from pathlib import Path
from typing import List, Optional

from backend.src.domain.entities.blueprint import Blueprint
from backend.src.domain.entities.room import Room
from backend.src.domain.entities.wall import Wall
from backend.src.domain.value_objects.bounding_box import BoundingBox
from backend.src.domain.value_objects.coordinates import Coordinates
from backend.src.application.use_cases.generate_blueprint import GenerateBlueprintUseCase
from backend.src.infrastructure.image.pillow_renderer import PillowBlueprintRenderer


class FloorPlan:
    """
    High-level interface for creating floor plans.
    
    This class provides a convenient API for building blueprints
    programmatically.
    """
    
    def __init__(self, blueprint_id: str, width: float = 1000.0, height: float = 1000.0):
        """
        Initialize a new floor plan.
        
        Args:
            blueprint_id: Unique identifier for the blueprint
            width: Blueprint width in normalized units (default: 1000)
            height: Blueprint height in normalized units (default: 1000)
        """
        self._blueprint = Blueprint(id=blueprint_id, width=width, height=height)
    
    def add_room(self, x: float, y: float, width: float, height: float, name: Optional[str] = None) -> str:
        """
        Add a rectangular room to the floor plan.
        
        Args:
            x: X coordinate of room's top-left corner
            y: Y coordinate of room's top-left corner
            width: Room width
            height: Room height
            name: Optional room name
            
        Returns:
            Generated room ID
        """
        room_id = f"room_{len(self._blueprint.rooms) + 1:03d}"
        bbox = BoundingBox(
            x_min=x,
            y_min=y,
            x_max=x + width,
            y_max=y + height
        )
        room = Room(id=room_id, bounding_box=bbox, name_hint=name)
        self._blueprint.add_room(room)
        return room_id
    
    def add_wall(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                 thickness: float = 5.0, is_load_bearing: bool = False) -> str:
        """
        Add a wall segment to the floor plan.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            thickness: Wall thickness (default: 5.0)
            is_load_bearing: Whether wall is load-bearing (default: False)
            
        Returns:
            Generated wall ID
        """
        wall_id = f"wall_{len(self._blueprint.walls) + 1:03d}"
        wall = Wall(
            id=wall_id,
            start=Coordinates(start_x, start_y),
            end=Coordinates(end_x, end_y),
            thickness=thickness,
            is_load_bearing=is_load_bearing
        )
        self._blueprint.add_wall(wall)
        return wall_id
    
    def add_rectangular_room_with_walls(self, x: float, y: float, width: float, height: float,
                                       name: Optional[str] = None, wall_thickness: float = 5.0) -> str:
        """
        Add a rectangular room with surrounding walls.
        
        This is a convenience method that creates both the room and its walls.
        
        Args:
            x: X coordinate of room's top-left corner
            y: Y coordinate of room's top-left corner
            width: Room width
            height: Room height
            name: Optional room name
            wall_thickness: Wall thickness (default: 5.0)
            
        Returns:
            Generated room ID
        """
        # Add room
        room_id = self.add_room(x, y, width, height, name)
        
        # Add walls around the room
        self.add_wall(x, y, x + width, y, wall_thickness)  # Top
        self.add_wall(x + width, y, x + width, y + height, wall_thickness)  # Right
        self.add_wall(x + width, y + height, x, y + height, wall_thickness)  # Bottom
        self.add_wall(x, y + height, x, y, wall_thickness)  # Left
        
        return room_id
    
    def get_blueprint(self) -> Blueprint:
        """Get the underlying blueprint entity."""
        return self._blueprint
    
    def to_json(self) -> dict:
        """Convert floor plan to JSON representation."""
        return self._blueprint.to_dict()


def generate_blueprint_image(blueprint: Blueprint, output_path: str, 
                            image_width: int = 1000, image_height: int = 1000) -> str:
    """
    Generate a blueprint image from a blueprint entity.
    
    Args:
        blueprint: The blueprint entity to render
        output_path: Path where the image should be saved
        image_width: Output image width in pixels (default: 1000)
        image_height: Output image height in pixels (default: 1000)
        
    Returns:
        Path to the generated image file
    """
    renderer = PillowBlueprintRenderer(
        image_width=image_width,
        image_height=image_height,
        background_color="white",
        wall_color="black",
        room_color=None  # No room fill for now
    )
    
    use_case = GenerateBlueprintUseCase(renderer)
    return use_case.execute(blueprint, output_path)


def create_simple_rectangular_room(blueprint_id: str, x: float, y: float, 
                                   width: float, height: float, name: Optional[str] = None) -> Blueprint:
    """
    Create a simple blueprint with a single rectangular room.
    
    Args:
        blueprint_id: Unique identifier for the blueprint
        x: X coordinate of room's top-left corner
        y: Y coordinate of room's top-left corner
        width: Room width
        height: Room height
        name: Optional room name
        
    Returns:
        Blueprint entity
    """
    floor_plan = FloorPlan(blueprint_id)
    floor_plan.add_rectangular_room_with_walls(x, y, width, height, name)
    return floor_plan.get_blueprint()


if __name__ == "__main__":
    # Example usage
    print("Generating example blueprint...")
    
    # Create a simple floor plan
    floor_plan = FloorPlan("example_001")
    
    # Add rooms with walls
    floor_plan.add_rectangular_room_with_walls(100, 100, 300, 400, "Living Room")
    floor_plan.add_rectangular_room_with_walls(450, 100, 300, 400, "Kitchen")
    
    # Generate blueprint
    blueprint = floor_plan.get_blueprint()
    output_path = Path(__file__).parent.parent / "blueprints" / "example_001.png"
    
    generate_blueprint_image(blueprint, str(output_path))
    print(f"Blueprint generated: {output_path}")

