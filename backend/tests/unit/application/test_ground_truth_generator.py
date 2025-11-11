"""Unit tests for Ground Truth Generator."""

import json
import tempfile
from pathlib import Path

import pytest

from backend.src.domain.entities.blueprint import Blueprint
from backend.src.domain.entities.room import Room
from backend.src.domain.value_objects.bounding_box import BoundingBox
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from data_generation.scripts.ground_truth_generator import GroundTruthGenerator


class TestGroundTruthGenerator:
    """Test suite for Ground Truth Generator."""
    
    def test_generate_from_blueprint(self):
        """Test generating ground truth from blueprint."""
        # Create a simple blueprint with one room
        blueprint = Blueprint(id="test_001")
        room = Room(
            id="room_001",
            bounding_box=BoundingBox(x_min=100, y_min=200, x_max=500, y_max=600),
            name_hint="Kitchen"
        )
        blueprint.add_room(room)
        
        # Generate ground truth
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_001_ground_truth.json"
            ground_truth = GroundTruthGenerator.generate_from_blueprint(blueprint, str(output_path))
            
            # Check structure
            assert ground_truth["blueprint_id"] == "test_001"
            assert ground_truth["metadata"]["room_count"] == 1
            assert len(ground_truth["ground_truth"]) == 1
            assert ground_truth["ground_truth"][0]["id"] == "room_001"
            assert ground_truth["ground_truth"][0]["name_hint"] == "Kitchen"
            
            # Check file was created
            assert output_path.exists()
    
    def test_validate_ground_truth_valid(self):
        """Test validation of valid ground truth."""
        valid_ground_truth = {
            "blueprint_id": "test_001",
            "image_path": "blueprints/test_001.png",
            "metadata": {
                "width": 1000,
                "height": 1000,
                "room_count": 1
            },
            "ground_truth": [
                {
                    "id": "room_001",
                    "bounding_box": [100, 200, 500, 600],
                    "name_hint": "Kitchen"
                }
            ]
        }
        
        assert GroundTruthGenerator.validate_ground_truth(valid_ground_truth) is True
    
    def test_validate_ground_truth_missing_field(self):
        """Test validation fails for missing required field."""
        invalid = {
            "blueprint_id": "test_001",
            # Missing image_path
            "metadata": {},
            "ground_truth": []
        }
        
        with pytest.raises(ValueError, match="Missing required field"):
            GroundTruthGenerator.validate_ground_truth(invalid)
    
    def test_validate_ground_truth_invalid_bbox(self):
        """Test validation fails for invalid bounding box."""
        invalid = {
            "blueprint_id": "test_001",
            "image_path": "blueprints/test_001.png",
            "metadata": {
                "width": 1000,
                "height": 1000,
                "room_count": 1
            },
            "ground_truth": [
                {
                    "id": "room_001",
                    "bounding_box": [500, 200, 100, 600]  # x_min > x_max
                }
            ]
        }
        
        with pytest.raises(ValueError, match="invalid bounding box geometry"):
            GroundTruthGenerator.validate_ground_truth(invalid)
    
    def test_load_ground_truth(self):
        """Test loading ground truth from file."""
        ground_truth_data = {
            "blueprint_id": "test_001",
            "image_path": "blueprints/test_001.png",
            "metadata": {
                "width": 1000,
                "height": 1000,
                "room_count": 1
            },
            "ground_truth": [
                {
                    "id": "room_001",
                    "bounding_box": [100, 200, 500, 600]
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            with open(file_path, 'w') as f:
                json.dump(ground_truth_data, f)
            
            loaded = GroundTruthGenerator.load_ground_truth(str(file_path))
            assert loaded == ground_truth_data

