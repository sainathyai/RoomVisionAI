"""Use case for detecting rooms from blueprint images."""

import time
from typing import List, Dict, Optional

from PIL import Image

from ...domain.interfaces.blueprint_renderer import BlueprintRenderer
from ...infrastructure.aws.bedrock_client import BedrockClient
from ...infrastructure.image.image_processor import ImageProcessor
from ...infrastructure.parsers.response_parser import ResponseParser
from ..validators.room_validator import RoomValidator
from ..prompts import get_prompt_for_blueprint


class DetectRoomsUseCase:
    """
    Use case for detecting rooms from blueprint images using vision LLM.
    
    Orchestrates the complete room detection pipeline:
    1. Image preprocessing
    2. Vision LLM inference
    3. Response parsing
    4. Validation
    """
    
    def __init__(
        self,
        bedrock_client: BedrockClient,
        image_processor: Optional[ImageProcessor] = None,
        response_parser: Optional[ResponseParser] = None,
        room_validator: Optional[RoomValidator] = None
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            bedrock_client: Bedrock client for vision inference
            image_processor: Image preprocessing (default: ImageProcessor())
            response_parser: Response parser (default: ResponseParser())
            room_validator: Room validator (default: RoomValidator())
        """
        self._bedrock_client = bedrock_client
        self._image_processor = image_processor or ImageProcessor()
        self._response_parser = response_parser or ResponseParser()
        self._room_validator = room_validator or RoomValidator()
    
    def execute(
        self,
        image: Image.Image,
        complexity: str = "standard",
        has_small_text: bool = False
    ) -> Dict:
        """
        Execute room detection on blueprint image.
        
        Args:
            image: Blueprint image (PIL Image)
            complexity: Blueprint complexity ("simple", "standard", "complex")
            has_small_text: Whether blueprint has small/unclear text
            
        Returns:
            Dictionary with:
            - success: bool
            - rooms: List[Dict] - Detected rooms
            - processing_time: float - Processing time in seconds
            - error: Optional[str] - Error message if failed
        """
        start_time = time.time()
        
        try:
            # 1. Preprocess image
            processed_image = self._image_processor.preprocess_blueprint(image)
            
            # 2. Get appropriate prompt
            prompt = get_prompt_for_blueprint(complexity=complexity, has_small_text=has_small_text)
            
            # 3. Invoke vision model
            response_text = self._bedrock_client.invoke_vision_model(processed_image, prompt)
            
            # 4. Parse response
            rooms_data = self._response_parser.sanitize_response(response_text)
            
            # 5. Validate rooms
            valid_rooms = self._room_validator.validate_rooms(rooms_data)
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "rooms": valid_rooms,
                "processing_time": processing_time,
                "error": None
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "success": False,
                "rooms": [],
                "processing_time": processing_time,
                "error": str(e)
            }

