"""
Generate Level 3, 4, and 5 test datasets with complex variations.

Level 3: Complex shapes (L-shaped, angled walls, open floor plans)
Level 4: Real-world challenges (small text, varying styles, furniture)
Level 5: Edge cases (no labels, tiny rooms, irregular shapes)
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_generation.scripts.blueprint_generator import FloorPlan, generate_blueprint_image
from data_generation.scripts.ground_truth_generator import generate_ground_truth_for_blueprint


class AdvancedTestSuiteGenerator:
    """Generates advanced test datasets with complex variations."""
    
    def __init__(self, output_dir=None):
        """Initialize generator."""
        if output_dir is None:
            output_dir = project_root / "data-generation"
        self.output_dir = Path(output_dir)
        self.blueprints_dir = self.output_dir / "blueprints"
        self.ground_truth_dir = self.output_dir / "ground-truth"
        self.blueprints_dir.mkdir(parents=True, exist_ok=True)
        self.ground_truth_dir.mkdir(parents=True, exist_ok=True)
        self.generated_blueprints = []
    
    def generate_level_3_complex_shapes(self):
        """Level 3: Complex shapes (15 blueprints)."""
        blueprints = []
        
        # Test 26: L-shaped room
        fp = FloorPlan("level3_test_026")
        # Create L-shape with walls
        fp.add_wall(100, 100, 500, 100)  # Top horizontal
        fp.add_wall(500, 100, 500, 400)  # Right vertical (top)
        fp.add_wall(500, 400, 800, 400)  # Middle horizontal
        fp.add_wall(800, 400, 800, 700)  # Right vertical (bottom)
        fp.add_wall(800, 700, 100, 700)  # Bottom horizontal
        fp.add_wall(100, 700, 100, 100)  # Left vertical
        # Add room covering L-shape
        fp.add_room(100, 100, 700, 600, "L-Shaped Room")
        blueprints.append(self._save_blueprint(fp, "L-shaped room"))
        
        # Test 27: U-shaped room
        fp = FloorPlan("level3_test_027")
        fp.add_wall(100, 100, 700, 100)  # Top
        fp.add_wall(700, 100, 700, 300)  # Right top
        fp.add_wall(700, 500, 700, 700)  # Right bottom
        fp.add_wall(100, 700, 700, 700)  # Bottom
        fp.add_wall(100, 100, 100, 700)  # Left
        fp.add_wall(700, 300, 500, 300)  # Inner right
        fp.add_wall(500, 500, 700, 500)  # Inner left
        fp.add_wall(500, 300, 500, 500)  # Inner bottom
        fp.add_room(100, 100, 600, 600, "U-Shaped Room")
        blueprints.append(self._save_blueprint(fp, "U-shaped room"))
        
        # Test 28: Open floor plan (large room with internal divisions)
        fp = FloorPlan("level3_test_028")
        fp.add_rectangular_room_with_walls(50, 50, 900, 800, "Open Living Space")
        # Add partial walls for visual division
        fp.add_wall(400, 200, 400, 400, thickness=3)  # Partial wall 1
        fp.add_wall(600, 500, 600, 700, thickness=3)  # Partial wall 2
        blueprints.append(self._save_blueprint(fp, "Open floor plan"))
        
        # Test 29: Angled walls (45 degrees)
        fp = FloorPlan("level3_test_029")
        # Create diamond-shaped room
        fp.add_wall(500, 100, 800, 400)  # Top-right
        fp.add_wall(800, 400, 500, 700)  # Bottom-right
        fp.add_wall(500, 700, 200, 400)  # Bottom-left
        fp.add_wall(200, 400, 500, 100)  # Top-left
        fp.add_room(200, 100, 600, 600, "Diamond Room")
        blueprints.append(self._save_blueprint(fp, "Angled walls (45 degrees)"))
        
        # Test 30: Multiple L-shaped rooms
        fp = FloorPlan("level3_test_030")
        # L-shape 1
        fp.add_wall(50, 50, 400, 50)
        fp.add_wall(400, 50, 400, 300)
        fp.add_wall(400, 300, 600, 300)
        fp.add_wall(600, 300, 600, 500)
        fp.add_wall(50, 500, 600, 500)
        fp.add_wall(50, 50, 50, 500)
        fp.add_room(50, 50, 550, 450, "L-Room 1")
        # L-shape 2
        fp.add_wall(650, 50, 950, 50)
        fp.add_wall(950, 50, 950, 400)
        fp.add_wall(650, 400, 950, 400)
        fp.add_wall(650, 400, 650, 700)
        fp.add_wall(650, 700, 950, 700)
        fp.add_wall(950, 400, 950, 700)
        fp.add_room(650, 50, 300, 650, "L-Room 2")
        blueprints.append(self._save_blueprint(fp, "Multiple L-shaped rooms"))
        
        # Test 31: T-shaped room
        fp = FloorPlan("level3_test_031")
        fp.add_wall(100, 100, 700, 100)  # Top
        fp.add_wall(700, 100, 700, 400)  # Right top
        fp.add_wall(400, 400, 700, 400)  # Middle horizontal
        fp.add_wall(400, 400, 400, 800)  # Center vertical
        fp.add_wall(100, 800, 700, 800)  # Bottom
        fp.add_wall(100, 100, 100, 800)  # Left
        fp.add_room(100, 100, 600, 700, "T-Shaped Room")
        blueprints.append(self._save_blueprint(fp, "T-shaped room"))
        
        # Test 32: H-shaped layout
        fp = FloorPlan("level3_test_032")
        # Left vertical
        fp.add_rectangular_room_with_walls(50, 50, 300, 400, "Room A")
        # Right vertical
        fp.add_rectangular_room_with_walls(650, 50, 300, 400, "Room B")
        # Center horizontal
        fp.add_rectangular_room_with_walls(400, 200, 200, 200, "Room C")
        blueprints.append(self._save_blueprint(fp, "H-shaped layout"))
        
        # Test 33: Cross-shaped room
        fp = FloorPlan("level3_test_033")
        # Create cross with walls
        fp.add_wall(300, 50, 700, 50)  # Top
        fp.add_wall(700, 50, 700, 300)  # Right top
        fp.add_wall(500, 300, 700, 300)  # Right horizontal
        fp.add_wall(500, 300, 500, 700)  # Center vertical
        fp.add_wall(300, 700, 500, 700)  # Bottom horizontal
        fp.add_wall(300, 300, 300, 700)  # Left bottom
        fp.add_wall(300, 300, 500, 300)  # Left horizontal
        fp.add_wall(300, 50, 300, 300)  # Left top
        fp.add_room(300, 50, 400, 650, "Cross Room")
        blueprints.append(self._save_blueprint(fp, "Cross-shaped room"))
        
        # Test 34: Irregular pentagon
        fp = FloorPlan("level3_test_034")
        fp.add_wall(400, 100, 800, 200)
        fp.add_wall(800, 200, 700, 600)
        fp.add_wall(700, 600, 300, 700)
        fp.add_wall(300, 700, 200, 400)
        fp.add_wall(200, 400, 400, 100)
        fp.add_room(200, 100, 600, 600, "Pentagon Room")
        blueprints.append(self._save_blueprint(fp, "Irregular pentagon"))
        
        # Test 35: Split-level concept
        fp = FloorPlan("level3_test_035")
        fp.add_rectangular_room_with_walls(50, 50, 450, 400, "Upper Level")
        fp.add_rectangular_room_with_walls(550, 50, 400, 400, "Lower Level")
        fp.add_wall(500, 100, 500, 350, thickness=8)  # Thick dividing wall
        blueprints.append(self._save_blueprint(fp, "Split-level concept"))
        
        # Test 36: Curved wall simulation (using many small segments)
        fp = FloorPlan("level3_test_036")
        # Simulate curve with multiple wall segments
        for i in range(10):
            x1 = 100 + i * 80
            y1 = 100 + int(50 * (i / 10) ** 2)
            x2 = 100 + (i + 1) * 80
            y2 = 100 + int(50 * ((i + 1) / 10) ** 2)
            fp.add_wall(x1, y1, x2, y2, thickness=3)
        fp.add_wall(900, 150, 900, 700)
        fp.add_wall(100, 700, 900, 700)
        fp.add_wall(100, 100, 100, 700)
        fp.add_room(100, 100, 800, 600, "Curved Wall Room")
        blueprints.append(self._save_blueprint(fp, "Curved wall simulation"))
        
        # Test 37: Multiple angled rooms
        fp = FloorPlan("level3_test_037")
        # Room 1 - angled
        fp.add_wall(100, 100, 500, 100)
        fp.add_wall(500, 100, 600, 300)
        fp.add_wall(600, 300, 200, 400)
        fp.add_wall(200, 400, 100, 200)
        fp.add_wall(100, 200, 100, 100)
        fp.add_room(100, 100, 500, 300, "Angled Room 1")
        # Room 2 - different angle
        fp.add_wall(700, 100, 900, 200)
        fp.add_wall(900, 200, 850, 500)
        fp.add_wall(850, 500, 650, 400)
        fp.add_wall(650, 400, 700, 100)
        fp.add_room(650, 100, 250, 400, "Angled Room 2")
        blueprints.append(self._save_blueprint(fp, "Multiple angled rooms"))
        
        # Test 38: Complex multi-room with shared walls
        fp = FloorPlan("level3_test_038")
        fp.add_rectangular_room_with_walls(50, 50, 400, 350, "Room 1")
        fp.add_rectangular_room_with_walls(500, 50, 450, 350, "Room 2")
        fp.add_rectangular_room_with_walls(50, 450, 300, 450, "Room 3")
        fp.add_rectangular_room_with_walls(400, 450, 550, 450, "Room 4")
        # Shared internal walls
        fp.add_wall(450, 50, 450, 400, thickness=5)
        fp.add_wall(350, 450, 350, 900, thickness=5)
        blueprints.append(self._save_blueprint(fp, "Complex multi-room shared walls"))
        
        # Test 39: Asymmetric layout
        fp = FloorPlan("level3_test_039")
        fp.add_rectangular_room_with_walls(50, 50, 250, 300, "Small Room")
        fp.add_rectangular_room_with_walls(350, 50, 600, 500, "Large Room")
        fp.add_rectangular_room_with_walls(50, 400, 250, 550, "Medium Room")
        fp.add_rectangular_room_with_walls(1000, 50, -200, 900, "Negative Room")  # Will be clipped
        blueprints.append(self._save_blueprint(fp, "Asymmetric layout"))
        
        # Test 40: Nested rooms concept
        fp = FloorPlan("level3_test_040")
        fp.add_rectangular_room_with_walls(100, 100, 800, 700, "Outer Room")
        fp.add_rectangular_room_with_walls(300, 250, 500, 400, "Inner Room")
        blueprints.append(self._save_blueprint(fp, "Nested rooms concept"))
        
        return blueprints
    
    def generate_level_4_real_world_challenges(self):
        """Level 4: Real-world challenges (10 blueprints)."""
        blueprints = []
        
        # Test 41: Small text labels
        fp = FloorPlan("level4_test_041")
        fp.add_rectangular_room_with_walls(50, 50, 400, 500, "A")  # Single letter
        fp.add_rectangular_room_with_walls(500, 50, 450, 500, "BR1")  # Abbreviation
        blueprints.append(self._save_blueprint(fp, "Small text labels"))
        
        # Test 42: No labels (empty names)
        fp = FloorPlan("level4_test_042")
        fp.add_rectangular_room_with_walls(50, 50, 400, 500, None)  # No label
        fp.add_rectangular_room_with_walls(500, 50, 450, 500, None)
        fp.add_rectangular_room_with_walls(50, 600, 900, 300, None)
        blueprints.append(self._save_blueprint(fp, "No labels"))
        
        # Test 43: Varying wall thicknesses
        fp = FloorPlan("level4_test_043")
        fp.add_wall(50, 50, 500, 50, thickness=2)  # Thin
        fp.add_wall(500, 50, 500, 500, thickness=10)  # Thick
        fp.add_wall(500, 500, 50, 500, thickness=5)  # Medium
        fp.add_wall(50, 500, 50, 50, thickness=8)  # Medium-thick
        fp.add_room(50, 50, 450, 450, "Variable Walls")
        blueprints.append(self._save_blueprint(fp, "Varying wall thicknesses"))
        
        # Test 44: Very small rooms
        fp = FloorPlan("level4_test_044")
        fp.add_rectangular_room_with_walls(50, 50, 80, 80, "Closet")
        fp.add_rectangular_room_with_walls(200, 50, 100, 100, "Bath")
        fp.add_rectangular_room_with_walls(50, 200, 120, 90, "Storage")
        fp.add_rectangular_room_with_walls(250, 200, 700, 600, "Main Room")
        blueprints.append(self._save_blueprint(fp, "Very small rooms"))
        
        # Test 45: Very large room
        fp = FloorPlan("level4_test_045")
        fp.add_rectangular_room_with_walls(10, 10, 980, 980, "Warehouse")
        blueprints.append(self._save_blueprint(fp, "Very large room"))
        
        # Test 46: Dense layout (many small rooms)
        fp = FloorPlan("level4_test_046")
        for i in range(5):
            for j in range(5):
                x = 50 + i * 180
                y = 50 + j * 180
                fp.add_rectangular_room_with_walls(x, y, 150, 150, f"R{i}{j}")
        blueprints.append(self._save_blueprint(fp, "Dense layout (25 rooms)"))
        
        # Test 47: Long narrow rooms
        fp = FloorPlan("level4_test_047")
        fp.add_rectangular_room_with_walls(50, 50, 900, 100, "Hallway")
        fp.add_rectangular_room_with_walls(50, 200, 200, 700, "Corridor")
        fp.add_rectangular_room_with_walls(300, 200, 900, 250, "Passage")
        blueprints.append(self._save_blueprint(fp, "Long narrow rooms"))
        
        # Test 48: Mixed room sizes
        fp = FloorPlan("level4_test_048")
        fp.add_rectangular_room_with_walls(50, 50, 100, 100, "Tiny")
        fp.add_rectangular_room_with_walls(200, 50, 400, 300, "Small")
        fp.add_rectangular_room_with_walls(650, 50, 300, 400, "Medium")
        fp.add_rectangular_room_with_walls(50, 400, 900, 550, "Large")
        blueprints.append(self._save_blueprint(fp, "Mixed room sizes"))
        
        # Test 49: Overlapping concept (rooms share space)
        fp = FloorPlan("level4_test_049")
        fp.add_rectangular_room_with_walls(100, 100, 600, 500, "Room A")
        fp.add_rectangular_room_with_walls(400, 300, 800, 700, "Room B")
        blueprints.append(self._save_blueprint(fp, "Overlapping rooms"))
        
        # Test 50: Minimal walls (open concept)
        fp = FloorPlan("level4_test_050")
        # Only outer walls
        fp.add_wall(50, 50, 950, 50)
        fp.add_wall(950, 50, 950, 950)
        fp.add_wall(950, 950, 50, 950)
        fp.add_wall(50, 950, 50, 50)
        # One room covering entire space
        fp.add_room(50, 50, 900, 900, "Open Space")
        blueprints.append(self._save_blueprint(fp, "Minimal walls open concept"))
        
        return blueprints
    
    def generate_level_5_edge_cases(self):
        """Level 5: Edge cases (10 blueprints)."""
        blueprints = []
        
        # Test 51: Single pixel room (minimum size)
        fp = FloorPlan("level5_test_051")
        fp.add_rectangular_room_with_walls(100, 100, 1, 1, "Tiny")
        fp.add_rectangular_room_with_walls(200, 100, 500, 600, "Normal")
        blueprints.append(self._save_blueprint(fp, "Minimum size room"))
        
        # Test 52: Rooms at boundaries (0,0 and 1000,1000)
        fp = FloorPlan("level5_test_052")
        fp.add_rectangular_room_with_walls(0, 0, 300, 300, "Corner 1")
        fp.add_rectangular_room_with_walls(700, 700, 300, 300, "Corner 2")
        blueprints.append(self._save_blueprint(fp, "Boundary rooms"))
        
        # Test 53: Rooms with same coordinates
        fp = FloorPlan("level5_test_053")
        fp.add_rectangular_room_with_walls(100, 100, 400, 400, "Room 1")
        fp.add_rectangular_room_with_walls(100, 100, 400, 400, "Room 2")  # Same location
        blueprints.append(self._save_blueprint(fp, "Overlapping coordinates"))
        
        # Test 54: Very thin rooms
        fp = FloorPlan("level5_test_054")
        fp.add_rectangular_room_with_walls(50, 50, 900, 60, "Thin Horizontal")
        fp.add_rectangular_room_with_walls(50, 100, 60, 900, "Thin Vertical")
        blueprints.append(self._save_blueprint(fp, "Very thin rooms"))
        
        # Test 55: Maximum size room
        fp = FloorPlan("level5_test_055")
        fp.add_rectangular_room_with_walls(0, 0, 1000, 1000, "Max Room")
        blueprints.append(self._save_blueprint(fp, "Maximum size room"))
        
        # Test 56: Many tiny rooms
        fp = FloorPlan("level5_test_056")
        for i in range(10):
            for j in range(10):
                x = i * 95
                y = j * 95
                fp.add_rectangular_room_with_walls(x, y, 90, 90, f"{i}{j}")
        blueprints.append(self._save_blueprint(fp, "100 tiny rooms"))
        
        # Test 57: Irregular spacing
        fp = FloorPlan("level5_test_057")
        fp.add_rectangular_room_with_walls(10, 10, 150, 200, "Room 1")
        fp.add_rectangular_room_with_walls(200, 15, 350, 195, "Room 2")  # Slight offset
        fp.add_rectangular_room_with_walls(400, 20, 550, 190, "Room 3")
        blueprints.append(self._save_blueprint(fp, "Irregular spacing"))
        
        # Test 58: Rooms with gaps
        fp = FloorPlan("level5_test_058")
        fp.add_rectangular_room_with_walls(50, 50, 400, 400, "Room 1")
        fp.add_rectangular_room_with_walls(500, 50, 450, 400, "Room 2")
        # Gap between rooms (no wall connection)
        blueprints.append(self._save_blueprint(fp, "Rooms with gaps"))
        
        # Test 59: Single wall room (invalid but test edge case)
        fp = FloorPlan("level5_test_059")
        fp.add_wall(100, 100, 500, 100)
        fp.add_room(100, 100, 400, 200, "Partial Room")
        blueprints.append(self._save_blueprint(fp, "Incomplete room"))
        
        # Test 60: Extreme aspect ratios
        fp = FloorPlan("level5_test_060")
        fp.add_rectangular_room_with_walls(50, 50, 900, 100, "Wide Room")
        fp.add_rectangular_room_with_walls(50, 200, 100, 800, "Tall Room")
        blueprints.append(self._save_blueprint(fp, "Extreme aspect ratios"))
        
        return blueprints
    
    def _save_blueprint(self, floor_plan: FloorPlan, description: str):
        """Save blueprint and return metadata."""
        blueprint = floor_plan.get_blueprint()
        
        image_path = self.blueprints_dir / f"{blueprint.id}.png"
        generate_blueprint_image(blueprint, str(image_path))
        
        generate_ground_truth_for_blueprint(blueprint, str(self.ground_truth_dir))
        
        metadata = {
            "id": blueprint.id,
            "description": description,
            "room_count": len(blueprint.rooms),
            "wall_count": len(blueprint.walls)
        }
        
        self.generated_blueprints.append(metadata)
        return metadata
    
    def generate_all(self):
        """Generate all advanced test datasets."""
        print("Generating Level 3: Complex Shapes...")
        level3 = self.generate_level_3_complex_shapes()
        print(f"Generated {len(level3)} blueprints")
        
        print("\nGenerating Level 4: Real-World Challenges...")
        level4 = self.generate_level_4_real_world_challenges()
        print(f"Generated {len(level4)} blueprints")
        
        print("\nGenerating Level 5: Edge Cases...")
        level5 = self.generate_level_5_edge_cases()
        print(f"Generated {len(level5)} blueprints")
        
        # Update manifest
        manifest_path = self.output_dir / "test_suite_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
        else:
            manifest = {"total_blueprints": 0, "levels": {}}
        
        manifest["levels"]["level_3"] = {
            "name": "Complex Shapes",
            "count": len(level3),
            "blueprints": level3
        }
        manifest["levels"]["level_4"] = {
            "name": "Real-World Challenges",
            "count": len(level4),
            "blueprints": level4
        }
        manifest["levels"]["level_5"] = {
            "name": "Edge Cases",
            "count": len(level5),
            "blueprints": level5
        }
        
        manifest["total_blueprints"] = manifest.get("total_blueprints", 0) + len(level3) + len(level4) + len(level5)
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n✅ Generated {len(level3) + len(level4) + len(level5)} additional blueprints")
        print(f"Total blueprints: {manifest['total_blueprints']}")
        print(f"Manifest updated: {manifest_path}")


if __name__ == "__main__":
    generator = AdvancedTestSuiteGenerator()
    generator.generate_all()

