# Data Generation Guide

## Overview

This guide explains how to generate synthetic blueprint test data for the Room Detection AI system.

## Quick Start

```bash
cd data-generation/scripts
python generate_test_suite.py        # Generate Level 1-2 (25 blueprints)
python generate_level_3_4_5.py       # Generate Level 3-5 (35 blueprints)
```

## Scripts

### 1. `blueprint_generator.py`

Core blueprint generation engine.

**Usage:**
```python
from blueprint_generator import FloorPlan, generate_blueprint_image

# Create floor plan
fp = FloorPlan("test_001")
fp.add_rectangular_room_with_walls(100, 100, 300, 400, "Kitchen")

# Generate blueprint
blueprint = fp.get_blueprint()
generate_blueprint_image(blueprint, "output.png")
```

### 2. `ground_truth_generator.py`

Generate ground truth JSON files.

**Usage:**
```python
from ground_truth_generator import generate_ground_truth_for_blueprint

generate_ground_truth_for_blueprint(blueprint, "ground-truth/")
```

### 3. `generate_test_suite.py`

Generate Level 1-2 test datasets.

**Output:**
- 25 blueprint PNG images
- 25 ground truth JSON files
- Test suite manifest

### 4. `generate_level_3_4_5.py`

Generate Level 3-5 advanced test datasets.

**Output:**
- 35 blueprint PNG images
- 35 ground truth JSON files
- Updated manifest

## Test Suite Structure

```
data-generation/
├── blueprints/          # PNG images
│   ├── level1_test_001.png
│   └── ...
├── ground-truth/        # JSON ground truth
│   ├── level1_test_001_ground_truth.json
│   └── ...
└── test_suite_manifest.json
```

## Creating Custom Blueprints

```python
from blueprint_generator import FloorPlan

fp = FloorPlan("custom_001", width=1000, height=1000)

# Add rooms
fp.add_rectangular_room_with_walls(50, 50, 400, 500, "Living Room")
fp.add_rectangular_room_with_walls(500, 50, 450, 500, "Kitchen")

# Add individual walls
fp.add_wall(100, 100, 500, 100, thickness=5)

# Generate
blueprint = fp.get_blueprint()
```

## Ground Truth Format

```json
{
  "blueprint_id": "test_001",
  "image_path": "blueprints/test_001.png",
  "metadata": {
    "width": 1000,
    "height": 1000,
    "room_count": 2
  },
  "ground_truth": [
    {
      "id": "room_001",
      "bounding_box": [100, 200, 500, 600],
      "name_hint": "Kitchen"
    }
  ]
}
```

## Validation

Validate ground truth files:
```python
from ground_truth_generator import GroundTruthGenerator

gt = GroundTruthGenerator.load_ground_truth("ground-truth/test_001_ground_truth.json")
GroundTruthGenerator.validate_ground_truth(gt)
```

## Tips

1. **Coordinate System**: All coordinates normalized to 0-1000
2. **Room IDs**: Use format `room_XXX` for consistency
3. **Wall Thickness**: Default 5, range 1-50
4. **Image Size**: Output is 1000x1000 pixels
5. **Labels**: Optional but recommended for testing

## Troubleshooting

**Issue**: Blueprint validation fails
- Check coordinates are within 0-1000 range
- Ensure walls don't extend beyond blueprint bounds

**Issue**: Image generation fails
- Verify PIL/Pillow is installed
- Check file permissions for output directory

**Issue**: Ground truth validation fails
- Ensure bounding boxes are valid (x_min < x_max, y_min < y_max)
- Check all required fields are present

