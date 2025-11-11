"""AWS Bedrock client implementation."""

import json
import base64
import io
import time
from typing import Optional
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from PIL import Image


class BedrockClient:
    """
    AWS Bedrock client for invoking Claude Vision model.
    
    Implements the vision service interface for room detection.
    """
    
    def __init__(
        self,
        model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        region: str = "us-east-1",
        max_retries: int = 3,
        timeout: int = 60
    ):
        """
        Initialize Bedrock client.
        
        Args:
            model_id: Bedrock model ID
            region: AWS region
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds
        """
        self.model_id = model_id
        self.region = region
        self.max_retries = max_retries
        self.timeout = timeout
        
        self._client = boto3.client('bedrock-runtime', region_name=region)
    
    def invoke_vision_model(self, image: Image.Image, prompt: str) -> str:
        """
        Invoke Bedrock vision model with image and prompt.
        
        Args:
            image: PIL Image object
            prompt: Text prompt for the model
            
        Returns:
            Model response text
            
        Raises:
            ClientError: If AWS API call fails
            ValueError: If image is invalid
        """
        # Convert image to base64
        image_base64 = self._image_to_base64(image)
        
        # Prepare request body
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        # Invoke with retry logic
        for attempt in range(self.max_retries):
            try:
                response = self._client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(request_body)
                )
                
                result = json.loads(response['body'].read())
                return result['content'][0]['text']
                
            except ClientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                raise
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string.
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64 encoded image string
        """
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        return base64.b64encode(image_bytes).decode('utf-8')

