"""
Ground Truth Generator - Generates expected output JSON for blueprints.

This module creates ground truth data matching the PRD schema for validation
and testing purposes.
"""

import json
from pathlib import Path
from typing import List, Optional

from backend.src.domain.entities.blueprint import Blueprint
from backend.src.domain.entities.room import Room
from backend.src.domain.value_objects.bounding_box import BoundingBox


class GroundTruthGenerator:
    """
    Generates ground truth JSON files from blueprint entities.
    
    Ground truth files contain the expected output format matching
    the PRD schema for room detection validation.
    """
    
    @staticmethod
    def generate_from_blueprint(blueprint: Blueprint, output_path: str) -> dict:
        """
        Generate ground truth JSON from a blueprint entity.
        
        Args:
            blueprint: The blueprint entity with rooms
            output_path: Path where JSON should be saved
            
        Returns:
            Ground truth dictionary
        """
        ground_truth = {
            "blueprint_id": blueprint.id,
            "image_path": f"blueprints/{blueprint.id}.png",
            "metadata": {
                "width": blueprint.width,
                "height": blueprint.height,
                "room_count": len(blueprint.rooms),
                "wall_count": len(blueprint.walls)
            },
            "ground_truth": [
                room.to_dict() for room in blueprint.rooms
            ]
        }
        
        # Save to file
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path_obj, 'w', encoding='utf-8') as f:
            json.dump(ground_truth, f, indent=2, ensure_ascii=False)
        
        return ground_truth
    
    @staticmethod
    def load_ground_truth(file_path: str) -> dict:
        """
        Load ground truth from JSON file.
        
        Args:
            file_path: Path to ground truth JSON file
            
        Returns:
            Ground truth dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def validate_ground_truth(ground_truth: dict) -> bool:
        """
        Validate ground truth structure matches PRD schema.
        
        Args:
            ground_truth: Ground truth dictionary to validate
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        # Check required top-level fields
        required_fields = ["blueprint_id", "image_path", "metadata", "ground_truth"]
        for field in required_fields:
            if field not in ground_truth:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate metadata
        metadata = ground_truth["metadata"]
        required_metadata = ["width", "height", "room_count"]
        for field in required_metadata:
            if field not in metadata:
                raise ValueError(f"Missing required metadata field: {field}")
        
        # Validate ground_truth is a list
        if not isinstance(ground_truth["ground_truth"], list):
            raise ValueError("ground_truth must be a list")
        
        # Validate each room entry
        for i, room in enumerate(ground_truth["ground_truth"]):
            if not isinstance(room, dict):
                raise ValueError(f"Room at index {i} must be a dictionary")
            
            # Check required room fields
            if "id" not in room:
                raise ValueError(f"Room at index {i} missing 'id' field")
            if "bounding_box" not in room:
                raise ValueError(f"Room at index {i} missing 'bounding_box' field")
            
            # Validate bounding box format
            bbox = room["bounding_box"]
            if not isinstance(bbox, list) or len(bbox) != 4:
                raise ValueError(f"Room {room['id']} bounding_box must be [x_min, y_min, x_max, y_max]")
            
            # Validate coordinates are in 0-1000 range
            for coord in bbox:
                if not (0 <= coord <= 1000):
                    raise ValueError(f"Room {room['id']} has coordinate outside 0-1000 range: {coord}")
            
            # Validate box geometry
            if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
                raise ValueError(f"Room {room['id']} has invalid bounding box geometry")
        
        return True


def generate_ground_truth_for_blueprint(blueprint: Blueprint, output_dir: str) -> str:
    """
    Convenience function to generate ground truth file for a blueprint.
    
    Args:
        blueprint: The blueprint entity
        output_dir: Directory where ground truth should be saved
        
    Returns:
        Path to generated ground truth file
    """
    output_path = Path(output_dir) / f"{blueprint.id}_ground_truth.json"
    GroundTruthGenerator.generate_from_blueprint(blueprint, str(output_path))
    return str(output_path)


if __name__ == "__main__":
    # Example usage
    from blueprint_generator import create_simple_rectangular_room
    
    print("Generating example ground truth...")
    
    blueprint = create_simple_rectangular_room(
        blueprint_id="example_001",
        x=100,
        y=100,
        width=300,
        height=400,
        name="Living Room"
    )
    
    output_path = Path(__file__).parent.parent / "ground-truth" / "example_001_ground_truth.json"
    ground_truth = GroundTruthGenerator.generate_from_blueprint(blueprint, str(output_path))
    
    # Validate
    GroundTruthGenerator.validate_ground_truth(ground_truth)
    
    print(f"Ground truth generated: {output_path}")
    print(f"Validated: {GroundTruthGenerator.validate_ground_truth(ground_truth)}")

