"""Use case for generating a blueprint from a floor plan definition."""

from typing import Protocol

from ...domain.entities.blueprint import Blueprint
from ...domain.interfaces.blueprint_renderer import BlueprintRenderer


class GenerateBlueprintUseCase:
    """
    Use case for generating a blueprint image from a floor plan definition.
    
    This orchestrates the domain logic and infrastructure to create
    a visual representation of a blueprint.
    """
    
    def __init__(self, renderer: BlueprintRenderer):
        """
        Initialize the use case with a blueprint renderer.
        
        Args:
            renderer: Implementation of BlueprintRenderer interface
        """
        self._renderer = renderer
    
    def execute(self, blueprint: Blueprint, output_path: str) -> str:
        """
        Generate a blueprint image from a blueprint entity.
        
        Args:
            blueprint: The blueprint entity to render
            output_path: Path where the image should be saved
            
        Returns:
            Path to the generated image file
            
        Raises:
            ValueError: If blueprint validation fails
        """
        # Validate blueprint layout
        blueprint.validate_layout()
        
        # Render blueprint using infrastructure
        return self._renderer.render(blueprint, output_path)

