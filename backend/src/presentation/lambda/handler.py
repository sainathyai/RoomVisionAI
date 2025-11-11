"""AWS Lambda handler for room detection API."""

import json
import base64
from typing import Dict, Any

from PIL import Image
import io

from ...application.use_cases.detect_rooms import DetectRoomsUseCase
from ...infrastructure.aws.bedrock_client import BedrockClient
from ...infrastructure.image.image_processor import ImageProcessor


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for room detection requests.
    
    Expected event format:
    {
        "body": base64_encoded_image or {"image": base64_string},
        "headers": {"content-type": "image/png" or "application/json"}
    }
    
    Returns:
    {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": JSON string with detection results
    }
    """
    try:
        # Extract image from event
        image = _extract_image_from_event(event)
        
        # Initialize dependencies
        bedrock_client = BedrockClient()
        use_case = DetectRoomsUseCase(bedrock_client)
        
        # Detect rooms
        result = use_case.execute(image)
        
        # Format response
        if result["success"]:
            response_body = {
                "success": True,
                "rooms": result["rooms"],
                "processing_time": result["processing_time"],
                "model": "claude-3.5-sonnet"
            }
            status_code = 200
        else:
            response_body = {
                "success": False,
                "error": result["error"],
                "rooms": []
            }
            status_code = 500
        
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "rooms": []
            })
        }


def _extract_image_from_event(event: Dict[str, Any]) -> Image.Image:
    """
    Extract image from Lambda event.
    
    Supports multiple formats:
    - Base64 encoded in body
    - JSON with base64 image field
    - Direct image bytes
    """
    body = event.get("body", "")
    content_type = event.get("headers", {}).get("content-type", "")
    
    # Handle base64 encoded image
    if isinstance(body, str):
        try:
            # Try to decode as base64
            image_bytes = base64.b64decode(body)
            return Image.open(io.BytesIO(image_bytes))
        except:
            # Try to parse as JSON
            try:
                body_json = json.loads(body)
                if "image" in body_json:
                    image_bytes = base64.b64decode(body_json["image"])
                    return Image.open(io.BytesIO(image_bytes))
            except:
                pass
    
    # Handle binary body
    if isinstance(body, bytes):
        return Image.open(io.BytesIO(body))
    
    raise ValueError("Could not extract image from event body")

