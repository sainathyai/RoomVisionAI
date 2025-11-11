"""
Prompt Engineering for Room Detection.

Contains optimized prompts for AWS Bedrock Claude Vision model
to detect rooms from architectural blueprints.
"""

# Base prompt template
ROOM_DETECTION_PROMPT = """You are an expert architectural analyst. Analyze this blueprint image and identify all distinct rooms.

TASK:
- Identify each enclosed space defined by walls
- Determine bounding box coordinates for each room
- Extract or infer room labels/types
- Return results as valid JSON

COORDINATE SYSTEM:
- Normalize all coordinates to 0-1000 range
- Format: [x_min, y_min, x_max, y_max]
- Origin (0,0) is top-left corner
- x increases rightward, y increases downward

OUTPUT FORMAT:
Return ONLY valid JSON array (no markdown, no explanation):
[
  {
    "id": "room_001",
    "bounding_box": [x_min, y_min, x_max, y_max],
    "name_hint": "Room Type or Label"
  }
]

RULES:
1. Each room must be a distinct enclosed space
2. Include all rooms including hallways, closets
3. Exclude outdoor areas
4. If no label visible, infer from context (size, fixtures, location)
5. Bounding boxes should be tight around room boundaries
6. Do not overlap bounding boxes unless rooms actually overlap

ACCURACY REQUIREMENTS:
- Coordinate precision: ±5 units acceptable
- Must detect at least 90% of visible rooms
- Prioritize accuracy over completeness

Return the JSON array now:"""

# Enhanced prompt with examples
ROOM_DETECTION_PROMPT_WITH_EXAMPLES = """You are an expert architectural analyst. Analyze this blueprint image and identify all distinct rooms.

TASK:
- Identify each enclosed space defined by walls
- Determine bounding box coordinates for each room
- Extract or infer room labels/types
- Return results as valid JSON

COORDINATE SYSTEM:
- Normalize all coordinates to 0-1000 range
- Format: [x_min, y_min, x_max, y_max]
- Origin (0,0) is top-left corner
- x increases rightward, y increases downward

EXAMPLE OUTPUT:
[
  {
    "id": "room_001",
    "bounding_box": [100, 100, 500, 600],
    "name_hint": "Living Room"
  },
  {
    "id": "room_002",
    "bounding_box": [550, 100, 900, 600],
    "name_hint": "Kitchen"
  }
]

RULES:
1. Each room must be a distinct enclosed space
2. Include all rooms including hallways, closets
3. Exclude outdoor areas
4. If no label visible, infer from context (size, fixtures, location)
5. Bounding boxes should be tight around room boundaries
6. Do not overlap bounding boxes unless rooms actually overlap
7. Walls define room boundaries - look for continuous wall lines
8. Doors and openings don't break room boundaries

ACCURACY REQUIREMENTS:
- Coordinate precision: ±5 units acceptable
- Must detect at least 90% of visible rooms
- Prioritize accuracy over completeness

Return ONLY the JSON array, no markdown, no explanation:"""

# Prompt for complex blueprints
COMPLEX_BLUEPRINT_PROMPT = """You are an expert architectural analyst. This is a complex blueprint with multiple rooms, possibly with irregular shapes.

ANALYSIS STEPS:
1. First, identify all wall boundaries
2. Group walls into enclosed spaces
3. For each enclosed space, determine the bounding box
4. Extract or infer room labels

COORDINATE SYSTEM:
- Normalize to 0-1000 range
- Format: [x_min, y_min, x_max, y_max]
- Top-left is (0,0)

SPECIAL CASES:
- L-shaped rooms: Use bounding box that encompasses entire L-shape
- Open floor plans: Treat as single room if no clear divisions
- Hallways: Include as separate rooms if clearly defined
- Closets: Include even if very small

OUTPUT FORMAT (JSON array only):
[
  {
    "id": "room_001",
    "bounding_box": [x_min, y_min, x_max, y_max],
    "name_hint": "Room Type"
  }
]

Return the JSON array now:"""

# Prompt for blueprints with small text
SMALL_TEXT_PROMPT = """You are an expert architectural analyst. This blueprint may have small or unclear text labels.

TASK:
- Identify all rooms by their spatial boundaries (walls)
- Extract text labels if visible and readable
- If text is unclear, infer room type from:
  * Room size and proportions
  * Location in floor plan
  * Adjacent rooms
  * Typical architectural patterns

COORDINATE SYSTEM:
- Normalize to 0-1000 range
- Format: [x_min, y_min, x_max, y_max]

OUTPUT (JSON array only):
[
  {
    "id": "room_001",
    "bounding_box": [x_min, y_min, x_max, y_max],
    "name_hint": "Inferred or Extracted Label"
  }
]

Focus on accurate bounding boxes even if labels are uncertain.
Return JSON array:"""


def get_prompt_for_blueprint(complexity: str = "standard", has_small_text: bool = False) -> str:
    """
    Get appropriate prompt based on blueprint characteristics.
    
    Args:
        complexity: "simple", "standard", or "complex"
        has_small_text: Whether blueprint has small/unclear text
        
    Returns:
        Prompt string
    """
    if has_small_text:
        return SMALL_TEXT_PROMPT
    
    if complexity == "complex":
        return COMPLEX_BLUEPRINT_PROMPT
    
    if complexity == "simple":
        return ROOM_DETECTION_PROMPT
    
    return ROOM_DETECTION_PROMPT_WITH_EXAMPLES


# Prompt version tracking
PROMPT_VERSIONS = {
    "v1": ROOM_DETECTION_PROMPT,
    "v2": ROOM_DETECTION_PROMPT_WITH_EXAMPLES,
    "v3": COMPLEX_BLUEPRINT_PROMPT,
    "v4": SMALL_TEXT_PROMPT
}

CURRENT_PROMPT_VERSION = "v2"

