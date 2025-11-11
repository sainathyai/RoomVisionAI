"""PIL/Pillow implementation of blueprint renderer."""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from ...domain.entities.blueprint import Blueprint
from ...domain.interfaces.blueprint_renderer import BlueprintRenderer


class PillowBlueprintRenderer(BlueprintRenderer):
    """
    PIL/Pillow-based implementation of BlueprintRenderer.
    
    Renders blueprints as PNG images with walls, rooms, and labels.
    """
    
    def __init__(
        self,
        image_width: int = 1000,
        image_height: int = 1000,
        background_color: str = "white",
        wall_color: str = "black",
        room_color: Optional[str] = None,
        font_path: Optional[str] = None
    ):
        """
        Initialize the renderer with configuration.
        
        Args:
            image_width: Output image width in pixels
            image_height: Output image height in pixels
            background_color: Background color (default: white)
            wall_color: Wall line color (default: black)
            room_color: Room fill color (optional, None = no fill)
            font_path: Path to font file (optional, uses default if None)
        """
        self._image_width = image_width
        self._image_height = image_height
        self._background_color = background_color
        self._wall_color = wall_color
        self._room_color = room_color
        self._font_path = font_path
    
    def render(self, blueprint: Blueprint, output_path: str) -> str:
        """
        Render a blueprint to a PNG image file.
        
        Args:
            blueprint: The blueprint entity to render
            output_path: Path where the image should be saved
            
        Returns:
            Path to the rendered image file
        """
        # Create image canvas
        img = Image.new('RGB', (self._image_width, self._image_height), self._background_color)
        draw = ImageDraw.Draw(img)
        
        # Scale factor: blueprint uses 0-1000 normalized, image uses pixel dimensions
        scale_x = self._image_width / blueprint.width
        scale_y = self._image_height / blueprint.height
        
        # Draw rooms first (if any, as background)
        if self._room_color and blueprint.rooms:
            for room in blueprint.rooms:
                self._draw_room(draw, room, scale_x, scale_y)
        
        # Draw walls on top
        for wall in blueprint.walls:
            self._draw_wall(draw, wall, scale_x, scale_y)
        
        # Draw room labels
        if blueprint.rooms:
            self._draw_labels(draw, blueprint, scale_x, scale_y)
        
        # Save image
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path_obj, 'PNG')
        
        return str(output_path_obj.absolute())
    
    def _draw_wall(self, draw: ImageDraw.Draw, wall, scale_x: float, scale_y: float) -> None:
        """Draw a wall segment on the canvas."""
        start_x = int(wall.start.x * scale_x)
        start_y = int(wall.start.y * scale_y)
        end_x = int(wall.end.x * scale_x)
        end_y = int(wall.end.y * scale_y)
        
        # Scale thickness
        thickness = max(1, int(wall.thickness * min(scale_x, scale_y)))
        
        draw.line(
            [(start_x, start_y), (end_x, end_y)],
            fill=self._wall_color,
            width=thickness
        )
    
    def _draw_room(self, draw: ImageDraw.Draw, room, scale_x: float, scale_y: float) -> None:
        """Draw a room bounding box on the canvas."""
        bbox = room.bounding_box
        x_min = int(bbox.x_min * scale_x)
        y_min = int(bbox.y_min * scale_y)
        x_max = int(bbox.x_max * scale_x)
        y_max = int(bbox.y_max * scale_y)
        
        # Draw filled rectangle with slight transparency effect
        # (PIL doesn't support alpha directly, so we use a lighter color)
        draw.rectangle(
            [(x_min, y_min), (x_max, y_max)],
            fill=self._room_color,
            outline=None
        )
    
    def _draw_labels(self, draw: ImageDraw.Draw, blueprint: Blueprint, scale_x: float, scale_y: float) -> None:
        """Draw room labels on the canvas."""
        try:
            if self._font_path:
                font = ImageFont.truetype(self._font_path, size=12)
            else:
                # Try to use default font, fallback to basic if not available
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
        except:
            font = None
        
        for room in blueprint.rooms:
            if room.name_hint:
                bbox = room.bounding_box
                center = bbox.center
                x = int(center.x * scale_x)
                y = int(center.y * scale_y)
                
                # Draw text
                draw.text(
                    (x, y),
                    room.name_hint,
                    fill="black",
                    font=font,
                    anchor="mm"  # Middle-center anchor
                )

