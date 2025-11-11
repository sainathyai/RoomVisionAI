"""Interface for blueprint rendering service."""

from abc import ABC, abstractmethod
from typing import Protocol

from ..entities.blueprint import Blueprint


class BlueprintRenderer(Protocol):
    """
    Protocol defining the interface for blueprint rendering.
    
    This allows the domain layer to define what it needs without
    depending on specific image library implementations.
    """
    
    @abstractmethod
    def render(self, blueprint: Blueprint, output_path: str) -> str:
        """
        Render a blueprint to an image file.
        
        Args:
            blueprint: The blueprint entity to render
            output_path: Path where the image should be saved
            
        Returns:
            Path to the rendered image file
        """
        pass

