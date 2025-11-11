"""Image preprocessing for blueprint analysis."""

import base64
import io
from typing import Union
from pathlib import Path

from PIL import Image, ImageEnhance


class ImageProcessor:
    """Processes and optimizes images for vision LLM analysis."""
    
    MAX_SIZE = 2048  # Maximum dimension for Bedrock
    DEFAULT_CONTRAST_FACTOR = 1.5
    
    @staticmethod
    def validate_image(image_data: bytes) -> bool:
        """
        Validate image data.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image.verify()
            return True
        except Exception as e:
            raise ValueError(f"Invalid image data: {e}")
    
    @staticmethod
    def preprocess_blueprint(image_data: Union[bytes, Image.Image, str, Path]) -> Image.Image:
        """
        Preprocess blueprint image for optimal analysis.
        
        Args:
            image_data: Image as bytes, PIL Image, file path, or Path object
            
        Returns:
            Preprocessed PIL Image
        """
        # Load image if needed
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, (str, Path)):
            image = Image.open(image_data)
        elif isinstance(image_data, Image.Image):
            image = image_data.copy()
        else:
            raise ValueError(f"Unsupported image type: {type(image_data)}")
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        image = ImageProcessor.resize_if_needed(image)
        
        # Enhance contrast for better wall detection
        image = ImageProcessor.enhance_contrast(image)
        
        return image
    
    @staticmethod
    def resize_if_needed(image: Image.Image, max_size: int = MAX_SIZE) -> Image.Image:
        """
        Resize image if it exceeds maximum size.
        
        Args:
            image: PIL Image
            max_size: Maximum dimension in pixels
            
        Returns:
            Resized image (or original if within limits)
        """
        width, height = image.size
        
        if width <= max_size and height <= max_size:
            return image
        
        # Calculate new size maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = DEFAULT_CONTRAST_FACTOR) -> Image.Image:
        """
        Enhance image contrast for better feature detection.
        
        Args:
            image: PIL Image
            factor: Contrast enhancement factor (1.0 = no change)
            
        Returns:
            Enhanced image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def convert_to_base64(image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string.
        
        Args:
            image: PIL Image
            
        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

