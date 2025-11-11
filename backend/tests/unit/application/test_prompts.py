"""Unit tests for prompt engineering."""

from backend.src.application.prompts import (
    get_prompt_for_blueprint,
    ROOM_DETECTION_PROMPT,
    ROOM_DETECTION_PROMPT_WITH_EXAMPLES,
    COMPLEX_BLUEPRINT_PROMPT,
    SMALL_TEXT_PROMPT,
    CURRENT_PROMPT_VERSION
)


class TestPrompts:
    """Test suite for prompt functions."""
    
    def test_get_prompt_simple(self):
        """Test getting prompt for simple blueprint."""
        prompt = get_prompt_for_blueprint(complexity="simple")
        assert prompt == ROOM_DETECTION_PROMPT
    
    def test_get_prompt_standard(self):
        """Test getting prompt for standard blueprint."""
        prompt = get_prompt_for_blueprint(complexity="standard")
        assert prompt == ROOM_DETECTION_PROMPT_WITH_EXAMPLES
    
    def test_get_prompt_complex(self):
        """Test getting prompt for complex blueprint."""
        prompt = get_prompt_for_blueprint(complexity="complex")
        assert prompt == COMPLEX_BLUEPRINT_PROMPT
    
    def test_get_prompt_small_text(self):
        """Test getting prompt for blueprint with small text."""
        prompt = get_prompt_for_blueprint(has_small_text=True)
        assert prompt == SMALL_TEXT_PROMPT
    
    def test_prompts_contain_keywords(self):
        """Test that prompts contain essential keywords."""
        keywords = ["bounding_box", "x_min", "y_min", "x_max", "y_max", "JSON"]
        
        for prompt in [ROOM_DETECTION_PROMPT, ROOM_DETECTION_PROMPT_WITH_EXAMPLES]:
            for keyword in keywords:
                assert keyword in prompt or keyword.replace("_", " ") in prompt
    
    def test_prompts_mention_coordinate_range(self):
        """Test that prompts mention 0-1000 coordinate range."""
        for prompt in [ROOM_DETECTION_PROMPT, ROOM_DETECTION_PROMPT_WITH_EXAMPLES]:
            assert "0-1000" in prompt or "1000" in prompt
    
    def test_current_prompt_version_exists(self):
        """Test that current prompt version is defined."""
        assert CURRENT_PROMPT_VERSION is not None
        assert isinstance(CURRENT_PROMPT_VERSION, str)

