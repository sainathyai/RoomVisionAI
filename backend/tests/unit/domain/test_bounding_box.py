"""Unit tests for BoundingBox value object."""

import pytest

from backend.src.domain.value_objects.bounding_box import BoundingBox
from backend.src.domain.value_objects.coordinates import Coordinates


class TestBoundingBox:
    """Test suite for BoundingBox value object."""
    
    def test_create_valid_bounding_box(self):
        """Test creating valid bounding box."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        assert bbox.x_min == 100
        assert bbox.y_min == 200
        assert bbox.x_max == 500
        assert bbox.y_max == 600
    
    def test_bounding_box_validation_x_min_greater_than_x_max(self):
        """Test validation fails when x_min >= x_max."""
        with pytest.raises(ValueError, match="x_min.*must be less than x_max"):
            BoundingBox(x_min=500, y_min=200, x_max=100, y_max=600)
    
    def test_bounding_box_validation_y_min_greater_than_y_max(self):
        """Test validation fails when y_min >= y_max."""
        with pytest.raises(ValueError, match="y_min.*must be less than y_max"):
            BoundingBox(x_min=100, y_min=600, x_max=500, y_max=200)
    
    def test_width_calculation(self):
        """Test width calculation."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        assert bbox.width == 400
    
    def test_height_calculation(self):
        """Test height calculation."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        assert bbox.height == 400
    
    def test_area_calculation(self):
        """Test area calculation."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        assert bbox.area == 160000  # 400 * 400
    
    def test_center_calculation(self):
        """Test center point calculation."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        center = bbox.center
        assert center.x == 300  # (100 + 500) / 2
        assert center.y == 400  # (200 + 600) / 2
        assert isinstance(center, Coordinates)
    
    def test_to_list(self):
        """Test conversion to list."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        assert bbox.to_list() == [100, 200, 500, 600]
    
    def test_from_list(self):
        """Test creation from list."""
        bbox = BoundingBox.from_list([100, 200, 500, 600])
        assert bbox.x_min == 100
        assert bbox.y_min == 200
        assert bbox.x_max == 500
        assert bbox.y_max == 600
    
    def test_from_list_invalid_length(self):
        """Test from_list fails with invalid list length."""
        with pytest.raises(ValueError, match="Expected 4 coordinates"):
            BoundingBox.from_list([100, 200, 500])
    
    def test_contains_point(self):
        """Test point containment check."""
        bbox = BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600)
        
        # Point inside
        assert bbox.contains(Coordinates(300, 400)) is True
        
        # Point on boundary
        assert bbox.contains(Coordinates(100, 200)) is True
        assert bbox.contains(Coordinates(500, 600)) is True
        
        # Point outside
        assert bbox.contains(Coordinates(50, 100)) is False
        assert bbox.contains(Coordinates(600, 700)) is False

