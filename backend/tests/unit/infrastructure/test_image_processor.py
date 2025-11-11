"""Unit tests for ImageProcessor."""

import io
from pathlib import Path

import pytest
from PIL import Image

from backend.src.infrastructure.image.image_processor import ImageProcessor


class TestImageProcessor:
    """Test suite for ImageProcessor."""
    
    def test_validate_image_valid(self):
        """Test validation of valid image."""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        
        assert ImageProcessor.validate_image(image_data) is True
    
    def test_validate_image_invalid(self):
        """Test validation fails for invalid image."""
        invalid_data = b"not an image"
        
        with pytest.raises(ValueError):
            ImageProcessor.validate_image(invalid_data)
    
    def test_preprocess_blueprint_from_bytes(self):
        """Test preprocessing from bytes."""
        img = Image.new('RGB', (100, 100), color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        
        result = ImageProcessor.preprocess_blueprint(image_data)
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGB'
    
    def test_preprocess_blueprint_from_pil(self):
        """Test preprocessing from PIL Image."""
        img = Image.new('RGBA', (100, 100), color='white')
        result = ImageProcessor.preprocess_blueprint(img)
        
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGB'  # Should convert to RGB
    
    def test_resize_if_needed_small(self):
        """Test resize doesn't change small images."""
        img = Image.new('RGB', (500, 500), color='white')
        result = ImageProcessor.resize_if_needed(img, max_size=2048)
        
        assert result.size == (500, 500)
    
    def test_resize_if_needed_large(self):
        """Test resize reduces large images."""
        img = Image.new('RGB', (3000, 2000), color='white')
        result = ImageProcessor.resize_if_needed(img, max_size=2048)
        
        assert result.width <= 2048
        assert result.height <= 2048
        # Check aspect ratio maintained
        assert abs((result.width / result.height) - (3000 / 2000)) < 0.1
    
    def test_enhance_contrast(self):
        """Test contrast enhancement."""
        img = Image.new('RGB', (100, 100), color='gray')
        result = ImageProcessor.enhance_contrast(img, factor=1.5)
        
        assert isinstance(result, Image.Image)
        assert result.size == img.size
    
    def test_convert_to_base64(self):
        """Test base64 conversion."""
        img = Image.new('RGB', (100, 100), color='white')
        base64_str = ImageProcessor.convert_to_base64(img)
        
        assert isinstance(base64_str, str)
        assert len(base64_str) > 0

