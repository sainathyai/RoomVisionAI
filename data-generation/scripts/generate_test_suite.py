"""
Test Suite Generator - Creates comprehensive test datasets with variations.

Generates 60+ blueprints across 5 complexity levels with many variations
for thorough testing of the room detection system.
"""

import json
from pathlib import Path
from typing import List, Dict

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_generation.scripts.blueprint_generator import FloorPlan, generate_blueprint_image
from data_generation.scripts.ground_truth_generator import GroundTruthGenerator, generate_ground_truth_for_blueprint


class TestSuiteGenerator:
    """Generates comprehensive test datasets with variations."""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize test suite generator.
        
        Args:
            output_dir: Base directory for output files (default: data-generation)
        """
        if output_dir is None:
            output_dir = project_root / "data-generation"
        self.output_dir = Path(output_dir)
        self.blueprints_dir = self.output_dir / "blueprints"
        self.ground_truth_dir = self.output_dir / "ground-truth"
        self.blueprints_dir.mkdir(parents=True, exist_ok=True)
        self.ground_truth_dir.mkdir(parents=True, exist_ok=True)
        
        self.generated_blueprints = []
    
    def generate_level_1_simple_rectangular(self) -> List[Dict]:
        """
        Level 1: Simple rectangular rooms (10 blueprints).
        - 2-4 rooms per blueprint
        - All rectangular shapes
        - Clear wall boundaries
        - Large, readable labels
        """
        blueprints = []
        
        # Test 1: Two rooms side by side
        fp = FloorPlan("level1_test_001")
        fp.add_rectangular_room_with_walls(50, 50, 400, 500, "Living Room")
        fp.add_rectangular_room_with_walls(500, 50, 400, 500, "Kitchen")
        blueprints.append(self._save_blueprint(fp, "Two rooms side by side"))
        
        # Test 2: Three rooms in a row
        fp = FloorPlan("level1_test_002")
        fp.add_rectangular_room_with_walls(50, 50, 250, 400, "Bedroom 1")
        fp.add_rectangular_room_with_walls(350, 50, 250, 400, "Bedroom 2")
        fp.add_rectangular_room_with_walls(650, 50, 250, 400, "Bathroom")
        blueprints.append(self._save_blueprint(fp, "Three rooms in a row"))
        
        # Test 3: Four rooms in a grid (2x2)
        fp = FloorPlan("level1_test_003")
        fp.add_rectangular_room_with_walls(50, 50, 400, 400, "Kitchen")
        fp.add_rectangular_room_with_walls(500, 50, 400, 400, "Dining Room")
        fp.add_rectangular_room_with_walls(50, 500, 400, 400, "Living Room")
        fp.add_rectangular_room_with_walls(500, 500, 400, 400, "Bedroom")
        blueprints.append(self._save_blueprint(fp, "Four rooms in 2x2 grid"))
        
        # Test 4: Two rooms stacked vertically
        fp = FloorPlan("level1_test_004")
        fp.add_rectangular_room_with_walls(200, 50, 600, 400, "Office")
        fp.add_rectangular_room_with_walls(200, 500, 600, 400, "Storage")
        blueprints.append(self._save_blueprint(fp, "Two rooms stacked"))
        
        # Test 5: Single large room
        fp = FloorPlan("level1_test_005")
        fp.add_rectangular_room_with_walls(100, 100, 800, 700, "Great Room")
        blueprints.append(self._save_blueprint(fp, "Single large room"))
        
        # Test 6: Three rooms with hallway
        fp = FloorPlan("level1_test_006")
        fp.add_rectangular_room_with_walls(50, 50, 300, 400, "Bedroom")
        fp.add_rectangular_room_with_walls(400, 50, 300, 400, "Bathroom")
        fp.add_rectangular_room_with_walls(750, 50, 200, 400, "Closet")
        fp.add_rectangular_room_with_walls(50, 500, 900, 100, "Hallway")
        blueprints.append(self._save_blueprint(fp, "Three rooms with hallway"))
        
        # Test 7: Four small rooms
        fp = FloorPlan("level1_test_007")
        fp.add_rectangular_room_with_walls(50, 50, 200, 200, "Closet 1")
        fp.add_rectangular_room_with_walls(300, 50, 200, 200, "Closet 2")
        fp.add_rectangular_room_with_walls(550, 50, 200, 200, "Closet 3")
        fp.add_rectangular_room_with_walls(800, 50, 150, 200, "Closet 4")
        blueprints.append(self._save_blueprint(fp, "Four small utility rooms"))
        
        # Test 8: Two large rooms
        fp = FloorPlan("level1_test_008")
        fp.add_rectangular_room_with_walls(50, 50, 450, 800, "Master Suite")
        fp.add_rectangular_room_with_walls(550, 50, 400, 800, "Guest Suite")
        blueprints.append(self._save_blueprint(fp, "Two large suites"))
        
        # Test 9: Five rooms in L-shape layout
        fp = FloorPlan("level1_test_009")
        fp.add_rectangular_room_with_walls(50, 50, 300, 300, "Kitchen")
        fp.add_rectangular_room_with_walls(400, 50, 300, 300, "Dining")
        fp.add_rectangular_room_with_walls(750, 50, 200, 300, "Pantry")
        fp.add_rectangular_room_with_walls(50, 400, 300, 500, "Living Room")
        fp.add_rectangular_room_with_walls(400, 400, 550, 500, "Family Room")
        blueprints.append(self._save_blueprint(fp, "Five rooms L-shape"))
        
        # Test 10: Three rooms with different sizes
        fp = FloorPlan("level1_test_010")
        fp.add_rectangular_room_with_walls(50, 50, 200, 300, "Small Room")
        fp.add_rectangular_room_with_walls(300, 50, 400, 500, "Medium Room")
        fp.add_rectangular_room_with_walls(750, 50, 200, 700, "Tall Room")
        blueprints.append(self._save_blueprint(fp, "Three rooms different sizes"))
        
        return blueprints
    
    def generate_level_2_multiple_rooms(self) -> List[Dict]:
        """
        Level 2: Multiple rooms (15 blueprints).
        - 5-8 rooms per blueprint
        - Mix of room sizes
        - Hallways and corridors
        - Standard residential layout
        """
        blueprints = []
        
        # Test 11: Standard apartment layout
        fp = FloorPlan("level2_test_011")
        fp.add_rectangular_room_with_walls(50, 50, 300, 400, "Bedroom 1")
        fp.add_rectangular_room_with_walls(400, 50, 300, 400, "Bedroom 2")
        fp.add_rectangular_room_with_walls(750, 50, 200, 200, "Bathroom")
        fp.add_rectangular_room_with_walls(750, 300, 200, 150, "Closet")
        fp.add_rectangular_room_with_walls(50, 500, 400, 400, "Living Room")
        fp.add_rectangular_room_with_walls(500, 500, 450, 300, "Kitchen")
        fp.add_rectangular_room_with_walls(500, 850, 450, 50, "Balcony")
        blueprints.append(self._save_blueprint(fp, "Standard apartment layout"))
        
        # Test 12: Office floor plan
        fp = FloorPlan("level2_test_012")
        fp.add_rectangular_room_with_walls(50, 50, 200, 200, "Office 1")
        fp.add_rectangular_room_with_walls(300, 50, 200, 200, "Office 2")
        fp.add_rectangular_room_with_walls(550, 50, 200, 200, "Office 3")
        fp.add_rectangular_room_with_walls(800, 50, 150, 200, "Office 4")
        fp.add_rectangular_room_with_walls(50, 300, 300, 400, "Conference Room")
        fp.add_rectangular_room_with_walls(400, 300, 250, 200, "Break Room")
        fp.add_rectangular_room_with_walls(700, 300, 250, 200, "Reception")
        fp.add_rectangular_room_with_walls(400, 550, 550, 150, "Hallway")
        blueprints.append(self._save_blueprint(fp, "Office floor plan"))
        
        # Test 13: House with garage
        fp = FloorPlan("level2_test_013")
        fp.add_rectangular_room_with_walls(50, 50, 300, 400, "Garage")
        fp.add_rectangular_room_with_walls(400, 50, 300, 300, "Entry")
        fp.add_rectangular_room_with_walls(750, 50, 200, 300, "Closet")
        fp.add_rectangular_room_with_walls(400, 400, 550, 400, "Living Room")
        fp.add_rectangular_room_with_walls(50, 500, 300, 350, "Kitchen")
        fp.add_rectangular_room_with_walls(400, 850, 300, 100, "Dining")
        fp.add_rectangular_room_with_walls(750, 400, 200, 550, "Bedroom")
        blueprints.append(self._save_blueprint(fp, "House with garage"))
        
        # Test 14: Multi-room suite
        fp = FloorPlan("level2_test_014")
        fp.add_rectangular_room_with_walls(50, 50, 400, 500, "Bedroom")
        fp.add_rectangular_room_with_walls(500, 50, 300, 300, "Bathroom")
        fp.add_rectangular_room_with_walls(850, 50, 100, 300, "Closet")
        fp.add_rectangular_room_with_walls(500, 400, 450, 150, "Sitting Area")
        fp.add_rectangular_room_with_walls(50, 600, 300, 350, "Study")
        fp.add_rectangular_room_with_walls(400, 600, 550, 350, "Living Area")
        blueprints.append(self._save_blueprint(fp, "Multi-room suite"))
        
        # Test 15: Hotel room layout
        fp = FloorPlan("level2_test_015")
        fp.add_rectangular_room_with_walls(50, 50, 400, 600, "Bedroom")
        fp.add_rectangular_room_with_walls(500, 50, 200, 250, "Bathroom")
        fp.add_rectangular_room_with_walls(750, 50, 200, 250, "Closet")
        fp.add_rectangular_room_with_walls(500, 350, 450, 300, "Living Area")
        fp.add_rectangular_room_with_walls(50, 700, 900, 250, "Balcony")
        blueprints.append(self._save_blueprint(fp, "Hotel room layout"))
        
        # Test 16: School classroom layout
        fp = FloorPlan("level2_test_016")
        fp.add_rectangular_room_with_walls(50, 50, 300, 400, "Classroom 1")
        fp.add_rectangular_room_with_walls(400, 50, 300, 400, "Classroom 2")
        fp.add_rectangular_room_with_walls(750, 50, 200, 400, "Storage")
        fp.add_rectangular_room_with_walls(50, 500, 200, 400, "Office")
        fp.add_rectangular_room_with_walls(300, 500, 400, 200, "Library")
        fp.add_rectangular_room_with_walls(300, 750, 400, 150, "Hallway")
        fp.add_rectangular_room_with_walls(750, 500, 200, 400, "Bathroom")
        blueprints.append(self._save_blueprint(fp, "School classroom layout"))
        
        # Test 17: Restaurant layout
        fp = FloorPlan("level2_test_017")
        fp.add_rectangular_room_with_walls(50, 50, 400, 500, "Dining Area 1")
        fp.add_rectangular_room_with_walls(500, 50, 450, 500, "Dining Area 2")
        fp.add_rectangular_room_with_walls(50, 600, 300, 350, "Kitchen")
        fp.add_rectangular_room_with_walls(400, 600, 200, 200, "Storage")
        fp.add_rectangular_room_with_walls(650, 600, 300, 200, "Bar")
        fp.add_rectangular_room_with_walls(400, 850, 200, 100, "Restroom")
        fp.add_rectangular_room_with_walls(650, 850, 300, 100, "Entrance")
        blueprints.append(self._save_blueprint(fp, "Restaurant layout"))
        
        # Test 18: Retail store
        fp = FloorPlan("level2_test_018")
        fp.add_rectangular_room_with_walls(50, 50, 400, 400, "Sales Floor 1")
        fp.add_rectangular_room_with_walls(500, 50, 450, 400, "Sales Floor 2")
        fp.add_rectangular_room_with_walls(50, 500, 300, 450, "Storage")
        fp.add_rectangular_room_with_walls(400, 500, 250, 200, "Office")
        fp.add_rectangular_room_with_walls(700, 500, 250, 200, "Break Room")
        fp.add_rectangular_room_with_walls(400, 750, 200, 200, "Restroom")
        fp.add_rectangular_room_with_walls(650, 750, 300, 200, "Checkout")
        blueprints.append(self._save_blueprint(fp, "Retail store"))
        
        # Test 19: Medical clinic
        fp = FloorPlan("level2_test_019")
        fp.add_rectangular_room_with_walls(50, 50, 250, 300, "Exam Room 1")
        fp.add_rectangular_room_with_walls(350, 50, 250, 300, "Exam Room 2")
        fp.add_rectangular_room_with_walls(650, 50, 300, 300, "Waiting Room")
        fp.add_rectangular_room_with_walls(50, 400, 300, 500, "Office")
        fp.add_rectangular_room_with_walls(400, 400, 300, 250, "Lab")
        fp.add_rectangular_room_with_walls(750, 400, 200, 250, "Storage")
        fp.add_rectangular_room_with_walls(400, 700, 300, 200, "Reception")
        fp.add_rectangular_room_with_walls(750, 700, 200, 200, "Restroom")
        blueprints.append(self._save_blueprint(fp, "Medical clinic"))
        
        # Test 20: Studio apartment
        fp = FloorPlan("level2_test_020")
        fp.add_rectangular_room_with_walls(50, 50, 600, 700, "Main Living")
        fp.add_rectangular_room_with_walls(700, 50, 250, 300, "Bathroom")
        fp.add_rectangular_room_with_walls(700, 400, 250, 200, "Closet")
        fp.add_rectangular_room_with_walls(50, 800, 300, 150, "Kitchen")
        fp.add_rectangular_room_with_walls(400, 800, 550, 150, "Dining")
        blueprints.append(self._save_blueprint(fp, "Studio apartment"))
        
        # Test 21: Two-bedroom apartment
        fp = FloorPlan("level2_test_021")
        fp.add_rectangular_room_with_walls(50, 50, 350, 400, "Bedroom 1")
        fp.add_rectangular_room_with_walls(450, 50, 350, 400, "Bedroom 2")
        fp.add_rectangular_room_with_walls(850, 50, 100, 200, "Bathroom")
        fp.add_rectangular_room_with_walls(850, 300, 100, 150, "Closet")
        fp.add_rectangular_room_with_walls(50, 500, 500, 400, "Living Room")
        fp.add_rectangular_room_with_walls(600, 500, 350, 250, "Kitchen")
        fp.add_rectangular_room_with_walls(600, 800, 350, 100, "Dining")
        blueprints.append(self._save_blueprint(fp, "Two-bedroom apartment"))
        
        # Test 22: Warehouse layout
        fp = FloorPlan("level2_test_022")
        fp.add_rectangular_room_with_walls(50, 50, 700, 600, "Warehouse Floor")
        fp.add_rectangular_room_with_walls(800, 50, 150, 300, "Office")
        fp.add_rectangular_room_with_walls(800, 400, 150, 250, "Break Room")
        fp.add_rectangular_room_with_walls(50, 700, 300, 250, "Loading Dock")
        fp.add_rectangular_room_with_walls(400, 700, 300, 250, "Storage")
        fp.add_rectangular_room_with_walls(750, 700, 200, 250, "Restroom")
        blueprints.append(self._save_blueprint(fp, "Warehouse layout"))
        
        # Test 23: Gym layout
        fp = FloorPlan("level2_test_023")
        fp.add_rectangular_room_with_walls(50, 50, 500, 500, "Main Gym")
        fp.add_rectangular_room_with_walls(600, 50, 350, 300, "Locker Room")
        fp.add_rectangular_room_with_walls(600, 400, 350, 150, "Shower")
        fp.add_rectangular_room_with_walls(50, 600, 300, 350, "Yoga Room")
        fp.add_rectangular_room_with_walls(400, 600, 250, 200, "Office")
        fp.add_rectangular_room_with_walls(700, 600, 250, 200, "Reception")
        fp.add_rectangular_room_with_walls(400, 850, 550, 100, "Hallway")
        blueprints.append(self._save_blueprint(fp, "Gym layout"))
        
        # Test 24: Library layout
        fp = FloorPlan("level2_test_024")
        fp.add_rectangular_room_with_walls(50, 50, 500, 600, "Reading Room")
        fp.add_rectangular_room_with_walls(600, 50, 350, 300, "Study Room 1")
        fp.add_rectangular_room_with_walls(600, 400, 350, 250, "Study Room 2")
        fp.add_rectangular_room_with_walls(50, 700, 300, 250, "Children's Area")
        fp.add_rectangular_room_with_walls(400, 700, 250, 250, "Office")
        fp.add_rectangular_room_with_walls(700, 700, 250, 250, "Reception")
        blueprints.append(self._save_blueprint(fp, "Library layout"))
        
        # Test 25: Co-working space
        fp = FloorPlan("level2_test_025")
        fp.add_rectangular_room_with_walls(50, 50, 400, 400, "Open Workspace")
        fp.add_rectangular_room_with_walls(500, 50, 450, 400, "Meeting Room")
        fp.add_rectangular_room_with_walls(50, 500, 300, 400, "Private Office 1")
        fp.add_rectangular_room_with_walls(400, 500, 300, 400, "Private Office 2")
        fp.add_rectangular_room_with_walls(750, 500, 200, 200, "Kitchen")
        fp.add_rectangular_room_with_walls(750, 750, 200, 150, "Restroom")
        blueprints.append(self._save_blueprint(fp, "Co-working space"))
        
        return blueprints
    
    def _save_blueprint(self, floor_plan: FloorPlan, description: str) -> Dict:
        """Save blueprint image and ground truth, return metadata."""
        blueprint = floor_plan.get_blueprint()
        
        # Generate image
        image_path = self.blueprints_dir / f"{blueprint.id}.png"
        generate_blueprint_image(blueprint, str(image_path))
        
        # Generate ground truth
        ground_truth_path = self.ground_truth_dir / f"{blueprint.id}_ground_truth.json"
        generate_ground_truth_for_blueprint(blueprint, str(self.ground_truth_dir))
        
        metadata = {
            "id": blueprint.id,
            "description": description,
            "image_path": str(image_path.relative_to(self.output_dir)),
            "ground_truth_path": str(ground_truth_path.relative_to(self.output_dir)),
            "room_count": len(blueprint.rooms),
            "wall_count": len(blueprint.walls)
        }
        
        self.generated_blueprints.append(metadata)
        return metadata
    
    def generate_all(self) -> Dict:
        """Generate all test datasets."""
        print("Generating Level 1: Simple Rectangular Rooms...")
        level1 = self.generate_level_1_simple_rectangular()
        print(f"Generated {len(level1)} blueprints")
        
        print("\nGenerating Level 2: Multiple Rooms...")
        level2 = self.generate_level_2_multiple_rooms()
        print(f"Generated {len(level2)} blueprints")
        
        # Save manifest
        manifest = {
            "total_blueprints": len(self.generated_blueprints),
            "levels": {
                "level_1": {
                    "name": "Simple Rectangular Rooms",
                    "count": len(level1),
                    "blueprints": level1
                },
                "level_2": {
                    "name": "Multiple Rooms",
                    "count": len(level2),
                    "blueprints": level2
                }
            }
        }
        
        manifest_path = self.output_dir / "test_suite_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n✅ Generated {len(self.generated_blueprints)} blueprints total")
        print(f"Manifest saved: {manifest_path}")
        
        return manifest


if __name__ == "__main__":
    generator = TestSuiteGenerator()
    generator.generate_all()

