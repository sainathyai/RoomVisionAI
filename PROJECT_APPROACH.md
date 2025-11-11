# Room Detection AI - Technical Approach & Implementation Strategy

## Executive Summary

This document outlines the technical approach for building the Room Detection AI system that automatically identifies and extracts room boundaries from architectural blueprints. We will leverage modern vision LLM technology through AWS Bedrock combined with prompt engineering to deliver a production-ready solution that meets the <30 second latency requirement without requiring extensive training data.

---

## 1. Core Approach: Vision LLM with Prompt Engineering

### 1.1 Why Prompt Engineering?

**Rationale:**
- ✅ **No training data required** - Works zero-shot on any blueprint
- ✅ **Rapid development** - Days instead of weeks/months
- ✅ **State-of-the-art accuracy** - Vision LLMs excel at spatial understanding
- ✅ **Meets latency requirements** - 5-15 second inference time
- ✅ **Usable product focus** - Production-ready vs. research project
- ✅ **Iterative improvement** - Easy to refine prompts based on results

**Key Innovation:**
Modern vision LLMs like Claude 3.5 Sonnet can understand complex visual layouts, spatial relationships, and architectural semantics - exactly what's needed for blueprint analysis.

---

## 2. Technology Stack

### 2.1 Primary AI Service: AWS Bedrock (Claude 3.5 Sonnet Vision)

**AWS Bedrock Overview:**
- Fully managed AWS AI/ML service (launched 2023)
- Hosts state-of-the-art foundation models
- Native AWS integration (IAM, CloudWatch, VPC, etc.)
- Pay-per-use pricing model

**Claude 3.5 Sonnet Vision Capabilities:**
- ✅ Image understanding and spatial reasoning
- ✅ Text extraction from images (OCR-like)
- ✅ Object detection and localization
- ✅ Structured output (JSON) generation
- ✅ Complex visual reasoning
- ✅ Coordinate extraction and spatial mapping

**Why Claude Vision?**
1. **Best-in-class vision understanding** - Outperforms GPT-4V on many benchmarks
2. **Excellent structured output** - Can reliably return JSON coordinates
3. **Spatial reasoning** - Understands room boundaries, walls, doors
4. **Text + visual fusion** - Can read labels AND understand layout
5. **Context window** - Can handle large blueprint images

### 2.2 Secondary Service: Amazon Textract (Optional Enhancement)

**Purpose:** Enhance text extraction accuracy if needed

**When to Use:**
- Blueprint has very small or unclear text labels
- Need higher confidence on room name extraction
- Parallel processing for text + boundary detection

**Integration Pattern:**
```
Primary: Bedrock → Room boundaries + labels
Fallback: Textract → Enhanced text extraction only
Merge: Combine results for maximum accuracy
```

### 2.3 Complete AWS Architecture

```
┌─────────────────┐
│   React App     │
│  (Frontend)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  API Gateway    │  ← REST API endpoint
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Lambda     │  ← Main processing logic
│  (Python 3.11)  │     - Image preprocessing
└────────┬────────┘     - Bedrock API calls
         │              - Response parsing
         │              - Validation
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│   S3   │ │ AWS Bedrock  │  ← Vision LLM inference
│Bucket  │ │(Claude Vision)│
└────────┘ └──────────────┘
    │
    ▼
┌────────────────┐
│  CloudWatch    │  ← Logging & monitoring
└────────────────┘
```

**Components:**

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **API Gateway** | REST API for frontend | CORS enabled, API key auth |
| **Lambda Function** | Orchestration & processing | Python 3.11, 512MB RAM, 60s timeout |
| **S3 Bucket** | Store uploaded blueprints | Versioning enabled, lifecycle policy |
| **Bedrock** | Vision LLM inference | Claude 3.5 Sonnet model |
| **CloudWatch** | Logs & metrics | Custom metrics for accuracy |
| **IAM Roles** | Security & permissions | Least privilege access |

### 2.4 Frontend Stack

**Technology:** React (as specified in PRD)

**Key Libraries:**
- **react-konva** or **fabric.js** - Canvas rendering for blueprint visualization
- **react-dropzone** - File upload interface
- **axios** - API communication
- **tailwindcss** - Modern UI styling

---

## 3. Data Synthesization Strategy

### 3.1 Why Synthetic Data?

**From PRD Section 5:**
> "To allow students to develop and test the core logic without access to proprietary Innergy blueprints, the project will use simplified mock data structure and public domain sample blueprints."

**Benefits of Synthetic Data:**
1. ✅ **Ground truth available** - Know exact expected output
2. ✅ **Unlimited test cases** - Generate as many as needed
3. ✅ **Controlled complexity** - Start simple, add complexity gradually
4. ✅ **No privacy concerns** - No proprietary blueprint data needed
5. ✅ **Reproducible testing** - Same data every time
6. ✅ **Edge case coverage** - Create specific challenging scenarios

### 3.2 Synthetic Blueprint Generation Process

#### **Step 1: Define Wall Structure (JSON)**

Generate programmatic floor plans as line segments:

```json
{
  "metadata": {
    "width": 1000,
    "height": 1000,
    "scale": "1:100",
    "units": "normalized"
  },
  "walls": [
    {"id": "w1", "start": [100, 100], "end": [900, 100], "thickness": 5},
    {"id": "w2", "start": [900, 100], "end": [900, 900], "thickness": 5},
    {"id": "w3", "start": [900, 900], "end": [100, 900], "thickness": 5},
    {"id": "w4", "start": [100, 900], "end": [100, 100], "thickness": 5},
    {"id": "w5", "start": [500, 100], "end": [500, 600], "thickness": 5}
  ],
  "doors": [
    {"id": "d1", "position": [500, 600], "wall_id": "w5", "width": 30}
  ],
  "labels": [
    {"text": "Living Room", "position": [250, 450], "font_size": 12},
    {"text": "Kitchen", "position": [700, 450], "font_size": 12}
  ]
}
```

#### **Step 2: Render to Blueprint Image**

**Using Python + PIL/Pillow:**

```python
from PIL import Image, ImageDraw, ImageFont

def generate_blueprint(wall_data, output_path):
    """Generate blueprint PNG from wall definition"""
    # Create white canvas
    img = Image.new('RGB', (1000, 1000), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw walls (black lines)
    for wall in wall_data['walls']:
        draw.line([wall['start'], wall['end']], 
                  fill='black', width=wall['thickness'])
    
    # Draw doors (dashed or different color)
    for door in wall_data['doors']:
        # Door rendering logic
        pass
    
    # Add text labels
    font = ImageFont.truetype("arial.ttf", 12)
    for label in wall_data['labels']:
        draw.text(label['position'], label['text'], 
                  fill='black', font=font)
    
    img.save(output_path)
    return output_path
```

#### **Step 3: Generate Ground Truth**

Create expected output JSON for validation:

```json
{
  "input_file": "blueprint_001.png",
  "ground_truth": [
    {
      "id": "room_001",
      "bounding_box": [100, 100, 500, 900],
      "name_hint": "Living Room",
      "area": 320000
    },
    {
      "id": "room_002",
      "bounding_box": [500, 100, 900, 600],
      "name_hint": "Kitchen",
      "area": 200000
    }
  ]
}
```

### 3.3 Test Data Generation Strategy

#### **Complexity Levels:**

**Level 1: Simple Rectangular Rooms (10 blueprints)**
- 2-4 rooms per floor
- All rectangular shapes
- Clear wall boundaries
- Large, readable labels

**Level 2: Multiple Rooms (15 blueprints)**
- 5-8 rooms per floor
- Mix of room sizes
- Hallways and corridors
- Standard residential layout

**Level 3: Complex Shapes (15 blueprints)**
- L-shaped rooms
- Open floor plans
- Angled walls (45°, 30°)
- Curved features (optional)

**Level 4: Real-World Challenges (10 blueprints)**
- Small text labels
- Furniture overlays
- Multiple floors (separate images)
- Varying blueprint styles (different line weights)

**Level 5: Edge Cases (10 blueprints)**
- Rooms without labels
- Overlapping spaces
- Very small utility rooms
- Irregular architectural features

#### **Total Dataset: 60 synthetic blueprints with ground truth**

### 3.4 Public Domain Blueprint Sources

Supplement synthetic data with real blueprints:

**Sources:**
1. **Wikimedia Commons** - Public domain architectural drawings
2. **Government archives** - Public building plans
3. **Educational resources** - Architecture school examples
4. **Creative Commons** - CC0 licensed floor plans

**Usage:**
- Use for final validation testing
- Test generalization to real blueprints
- Identify prompt improvements needed
- Demo real-world capability

---

## 4. Prompt Engineering Strategy

### 4.1 Core Prompt Template

```
You are an expert architectural analyst. Analyze this blueprint image and identify all distinct rooms.

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
```

### 4.2 Prompt Refinement Process

**Iteration Strategy:**

1. **Baseline Testing (Week 1)**
   - Test basic prompt on Level 1 simple blueprints
   - Measure accuracy against ground truth
   - Identify common errors (missed rooms, wrong coordinates, etc.)

2. **Prompt Enhancement (Week 1-2)**
   - Add specific instructions for error patterns
   - Include few-shot examples in prompt if needed
   - Adjust coordinate normalization instructions
   - Refine JSON structure requirements

3. **Advanced Testing (Week 2)**
   - Test on Level 2-3 complexity blueprints
   - Handle edge cases (L-shapes, angled walls)
   - Optimize for different blueprint styles

4. **Production Refinement (Week 3)**
   - Test on real public domain blueprints
   - Fine-tune for production accuracy
   - Add confidence scoring if needed

### 4.3 Multi-Stage Prompting (If Needed)

For complex blueprints, use two-stage approach:

**Stage 1: Analysis**
```
Analyze this blueprint and describe:
1. Overall layout (number of rooms, general structure)
2. Wall locations and orientations
3. Room labels visible in the image
4. Any challenging features (angled walls, complex shapes)
```

**Stage 2: Extraction**
```
Based on your analysis, now output the precise coordinates...
[Use main prompt template]
```

---

## 5. Implementation Pipeline

### 5.1 Request Flow

```
1. User uploads blueprint → React frontend
2. Frontend → POST /api/detect-rooms → API Gateway
3. API Gateway → Triggers Lambda function
4. Lambda:
   a. Validates image (size, format)
   b. Preprocesses image (resize if needed, enhance contrast)
   c. Converts to base64
   d. Calls Bedrock with prompt + image
   e. Parses LLM response
   f. Validates coordinates (0-1000 range, no NaN)
   g. Calculates confidence metrics
   h. Returns JSON response
5. Frontend receives JSON → Renders boxes on canvas
```

### 5.2 Lambda Function Structure

```python
# handler.py
import boto3
import json
import base64
from PIL import Image
import io

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # 1. Extract image from request
        image_data = extract_image(event)
        
        # 2. Preprocess image
        processed_image = preprocess_blueprint(image_data)
        
        # 3. Call Bedrock with vision prompt
        response = call_bedrock_vision(processed_image)
        
        # 4. Parse and validate response
        rooms = parse_and_validate(response)
        
        # 5. Return standardized response
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': True,
                'rooms': rooms,
                'processing_time': calculate_time(),
                'model': 'claude-3.5-sonnet'
            })
        }
    
    except Exception as e:
        return error_response(e)

def preprocess_blueprint(image_data):
    """Optimize image for vision LLM"""
    img = Image.open(io.BytesIO(image_data))
    
    # Resize if too large (max 5MB for Bedrock)
    if img.width > 2048 or img.height > 2048:
        img.thumbnail((2048, 2048), Image.LANCZOS)
    
    # Enhance contrast for better wall detection
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    return img

def call_bedrock_vision(image):
    """Call Bedrock Claude Vision API"""
    # Convert image to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Prepare request
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
                        "text": VISION_PROMPT  # Our engineered prompt
                    }
                ]
            }
        ]
    }
    
    # Call Bedrock
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps(request_body)
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

def parse_and_validate(llm_response):
    """Extract and validate JSON from LLM response"""
    # Extract JSON (handle markdown code blocks if present)
    json_str = extract_json(llm_response)
    rooms = json.loads(json_str)
    
    # Validate each room
    validated_rooms = []
    for room in rooms:
        if validate_room(room):
            validated_rooms.append(room)
    
    return validated_rooms

def validate_room(room):
    """Ensure room data is valid"""
    required_fields = ['id', 'bounding_box']
    
    # Check required fields
    if not all(field in room for field in required_fields):
        return False
    
    # Validate bounding box
    bbox = room['bounding_box']
    if len(bbox) != 4:
        return False
    
    # Check coordinate range (0-1000)
    if not all(0 <= coord <= 1000 for coord in bbox):
        return False
    
    # Check box validity (x_min < x_max, y_min < y_max)
    if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
        return False
    
    return True
```

### 5.3 Error Handling & Fallbacks

**Handling Common Issues:**

1. **LLM returns invalid JSON**
   - Retry with stricter prompt
   - Use JSON repair library
   - Return partial results if possible

2. **Coordinates out of range**
   - Clamp to 0-1000
   - Log warning for monitoring

3. **Missing room labels**
   - Return empty string for `name_hint`
   - Optional: Call Textract for text extraction

4. **Timeout (>30 seconds)**
   - Optimize image size
   - Use faster Bedrock model tier
   - Implement caching for repeated requests

---

## 6. Validation & Testing Strategy

### 6.1 Accuracy Metrics

**Intersection over Union (IoU):**
```python
def calculate_iou(pred_box, true_box):
    """Calculate overlap between predicted and ground truth"""
    x1 = max(pred_box[0], true_box[0])
    y1 = max(pred_box[1], true_box[1])
    x2 = min(pred_box[2], true_box[2])
    y2 = min(pred_box[3], true_box[3])
    
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    
    pred_area = (pred_box[2] - pred_box[0]) * (pred_box[3] - pred_box[1])
    true_area = (true_box[2] - true_box[0]) * (true_box[3] - true_box[1])
    
    union = pred_area + true_area - intersection
    
    return intersection / union if union > 0 else 0
```

**Success Criteria:**
- ✅ IoU > 0.75 for 80% of rooms
- ✅ Detection rate > 90% (find most rooms)
- ✅ False positive rate < 10%
- ✅ Processing time < 30 seconds

### 6.2 Testing Pipeline

```python
# test_suite.py
def run_validation_suite():
    """Test against all synthetic blueprints"""
    results = []
    
    for blueprint in get_test_blueprints():
        # Process blueprint
        predicted = process_blueprint(blueprint.image)
        ground_truth = blueprint.ground_truth
        
        # Calculate metrics
        metrics = {
            'blueprint_id': blueprint.id,
            'avg_iou': calculate_average_iou(predicted, ground_truth),
            'detection_rate': calculate_detection_rate(predicted, ground_truth),
            'false_positives': count_false_positives(predicted, ground_truth),
            'processing_time': blueprint.processing_time
        }
        
        results.append(metrics)
    
    # Generate report
    generate_report(results)
```

---

## 7. Hybrid Enhancement: When to Use Textract

### 7.1 Decision Logic

```python
def should_use_textract(bedrock_response, confidence_threshold=0.7):
    """Determine if Textract enhancement is needed"""
    
    # Count rooms with labels
    labeled_rooms = sum(1 for r in bedrock_response if r.get('name_hint'))
    total_rooms = len(bedrock_response)
    
    # If < 50% rooms have labels, try Textract
    if labeled_rooms / total_rooms < 0.5:
        return True
    
    # If confidence scores are low (if available)
    if 'confidence' in bedrock_response[0]:
        avg_confidence = sum(r['confidence'] for r in bedrock_response) / total_rooms
        if avg_confidence < confidence_threshold:
            return True
    
    return False
```

### 7.2 Textract Integration

```python
def enhance_with_textract(blueprint_image, bedrock_rooms):
    """Use Textract to extract additional text labels"""
    textract = boto3.client('textract')
    
    # Call Textract
    response = textract.detect_document_text(
        Document={'Bytes': blueprint_image}
    )
    
    # Extract text with positions
    text_items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_items.append({
                'text': block['Text'],
                'bbox': block['Geometry']['BoundingBox']
            })
    
    # Match text to rooms based on spatial proximity
    for room in bedrock_rooms:
        if not room.get('name_hint'):
            # Find closest text label
            closest_text = find_closest_text(room['bounding_box'], text_items)
            if closest_text:
                room['name_hint'] = closest_text
                room['label_source'] = 'textract'
    
    return bedrock_rooms
```

---

## 8. Performance Optimization

### 8.1 Latency Optimization

**Target: <30 seconds (requirement), Aim: <15 seconds**

**Optimization Strategies:**

1. **Image Preprocessing (1-2 seconds)**
   - Resize large images before sending
   - Compress without losing detail
   - Cache preprocessed versions

2. **Bedrock API Call (10-15 seconds)**
   - Use fastest model tier available
   - Optimize prompt length
   - Consider regional endpoints

3. **Response Processing (1-2 seconds)**
   - Efficient JSON parsing
   - Vectorized validation operations
   - Minimal post-processing

### 8.2 Cost Optimization

**Bedrock Pricing (approximate):**
- Input: ~$0.003 per 1K tokens
- Output: ~$0.015 per 1K tokens
- Image: ~1000 tokens per image

**Estimated Cost per Blueprint:**
- Image: ~$0.003
- Prompt: ~$0.001
- Response: ~$0.002
- **Total: ~$0.006 per blueprint**

**Cost Savings:**
- Cache results for identical blueprints
- Batch processing for multiple floors
- Use cheaper models for simple blueprints

---

## 9. Deliverables & Timeline

### 9.1 Week 1: Foundation
- ✅ Synthetic data generator (Python scripts)
- ✅ Generate 60 test blueprints with ground truth
- ✅ AWS account setup (Bedrock access, IAM roles)
- ✅ Initial prompt engineering (test with Claude)
- ✅ Baseline accuracy metrics

### 9.2 Week 2: Backend Development
- ✅ Lambda function implementation
- ✅ Bedrock API integration
- ✅ API Gateway setup
- ✅ Validation & testing pipeline
- ✅ Achieve >75% IoU on test set

### 9.3 Week 3: Frontend & Integration
- ✅ React application
- ✅ Blueprint upload interface
- ✅ Canvas visualization of detected rooms
- ✅ End-to-end integration testing
- ✅ Performance optimization

### 9.4 Week 4: Polish & Documentation
- ✅ Demo video (5-10 minutes)
- ✅ Technical writeup (2 pages)
- ✅ AWS setup documentation
- ✅ Code repository cleanup
- ✅ Final testing on public blueprints

---

## 10. Success Criteria

### 10.1 Technical Requirements
- ✅ Processing time: <30 seconds per blueprint
- ✅ Detection accuracy: >80% of rooms identified
- ✅ Coordinate precision: IoU >0.75 for 80% of rooms
- ✅ Valid JSON output: 100% parseable responses
- ✅ AWS-native: All services running on AWS

### 10.2 Deliverables Checklist
- ✅ Working code repository on GitHub
- ✅ Demo video showing end-to-end functionality
- ✅ Technical writeup (methodology, results, learnings)
- ✅ AWS documentation (architecture, setup guide)
- ✅ Synthetic test dataset (60 blueprints + ground truth)

### 10.3 Demonstration Capabilities
- ✅ Upload blueprint image via React UI
- ✅ Real-time processing (<30s)
- ✅ Display detected room boundaries on canvas
- ✅ Show room labels (if detected)
- ✅ Export results as JSON
- ✅ Handle various blueprint styles

---

## 11. Risk Mitigation

### 11.1 Potential Risks & Solutions

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Bedrock access denied | High | Low | Request access early, have GPT-4V backup |
| LLM accuracy insufficient | High | Medium | Iterate on prompts, add Textract, use synthetic data |
| Latency >30 seconds | Medium | Low | Optimize image size, use faster model tier |
| Cost overruns | Low | Low | Monitor usage, set billing alerts |
| Complex blueprints fail | Medium | Medium | Start simple, gradually increase complexity |

### 11.2 Backup Plans

**If Bedrock unavailable:**
- Use GPT-4 Vision via OpenAI API (call from Lambda)
- Still AWS-hosted (Lambda), just external AI service

**If vision LLM insufficient:**
- Implement traditional CV pipeline (OpenCV edge detection)
- Use AWS Rekognition Custom Labels (requires training data)

**If latency too high:**
- Implement async processing (S3 → Lambda → SNS notification)
- Show "processing" UI to user

---

## 12. Future Enhancements (Post-MVP)

### 12.1 Advanced Features
- **Multi-floor support** - Process entire building at once
- **3D visualization** - Render floor plans in 3D
- **Room area calculations** - Automatic square footage
- **Door/window detection** - Identify openings
- **Furniture detection** - Map existing furniture
- **Wall material inference** - Identify load-bearing walls

### 12.2 Production Improvements
- **Model fine-tuning** - Train custom model on Innergy blueprints
- **Active learning** - Learn from user corrections
- **Batch processing** - Process multiple floors efficiently
- **Real-time collaboration** - Multiple users editing simultaneously
- **Version control** - Track changes to floor plans

---

## Conclusion

This approach leverages cutting-edge vision LLM technology (AWS Bedrock + Claude Vision) combined with prompt engineering to deliver a production-ready room detection system. The use of synthetic data allows for rigorous testing without proprietary blueprints, while the AWS-native architecture ensures scalability, security, and compliance with project requirements.

**Key Advantages:**
1. ✅ Fast development (3-4 weeks vs. months)
2. ✅ No training data required (zero-shot learning)
3. ✅ State-of-the-art accuracy (vision LLM capabilities)
4. ✅ Fully AWS-compliant (Bedrock is AWS AI/ML service)
5. ✅ Production-ready (meets all latency and accuracy requirements)
6. ✅ Cost-effective (~$0.006 per blueprint)

**Next Steps:**
1. Set up AWS environment and Bedrock access
2. Build synthetic data generator
3. Begin prompt engineering experiments
4. Implement Lambda backend
5. Develop React frontend
6. Integrate and test end-to-end

---

**Document Version:** 1.0  
**Last Updated:** November 11, 2025  
**Project:** Room Detection AI - Gauntlet AI Week 4

