"""Unit tests for Coordinates value object."""

import pytest

from backend.src.domain.value_objects.coordinates import Coordinates


class TestCoordinates:
    """Test suite for Coordinates value object."""
    
    def test_create_valid_coordinates(self):
        """Test creating valid coordinates."""
        coords = Coordinates(x=100.0, y=200.0)
        assert coords.x == 100.0
        assert coords.y == 200.0
    
    def test_coordinates_are_immutable(self):
        """Test that coordinates are immutable (frozen dataclass)."""
        coords = Coordinates(x=100.0, y=200.0)
        with pytest.raises(Exception):  # dataclass.FrozenInstanceError
            coords.x = 200.0
    
    def test_coordinates_validation_x_min(self):
        """Test validation fails for x < 0."""
        with pytest.raises(ValueError, match="X coordinate must be between 0 and 1000"):
            Coordinates(x=-1, y=100)
    
    def test_coordinates_validation_x_max(self):
        """Test validation fails for x > 1000."""
        with pytest.raises(ValueError, match="X coordinate must be between 0 and 1000"):
            Coordinates(x=1001, y=100)
    
    def test_coordinates_validation_y_min(self):
        """Test validation fails for y < 0."""
        with pytest.raises(ValueError, match="Y coordinate must be between 0 and 1000"):
            Coordinates(x=100, y=-1)
    
    def test_coordinates_validation_y_max(self):
        """Test validation fails for y > 1000."""
        with pytest.raises(ValueError, match="Y coordinate must be between 0 and 1000"):
            Coordinates(x=100, y=1001)
    
    def test_coordinates_boundary_values(self):
        """Test that boundary values (0 and 1000) are valid."""
        coords1 = Coordinates(x=0, y=0)
        assert coords1.x == 0
        assert coords1.y == 0
        
        coords2 = Coordinates(x=1000, y=1000)
        assert coords2.x == 1000
        assert coords2.y == 1000
    
    def test_to_tuple(self):
        """Test conversion to tuple."""
        coords = Coordinates(x=100.0, y=200.0)
        assert coords.to_tuple() == (100.0, 200.0)
    
    def test_to_list(self):
        """Test conversion to list."""
        coords = Coordinates(x=100.0, y=200.0)
        assert coords.to_list() == [100.0, 200.0]
    
    def test_repr(self):
        """Test string representation."""
        coords = Coordinates(x=100.0, y=200.0)
        assert "Coordinates" in repr(coords)
        assert "100.0" in repr(coords)
        assert "200.0" in repr(coords)

