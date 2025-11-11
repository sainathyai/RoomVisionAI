# API Documentation

## Room Detection API

### Base URL
```
https://api.example.com
```

### Authentication
API Key required in header:
```
x-api-key: YOUR_API_KEY
```

## Endpoints

### POST /detect-rooms

Detect rooms from a blueprint image.

#### Request

**Headers:**
```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

**Body:**
```json
{
  "image": "base64_encoded_image_string",
  "filename": "blueprint.png"
}
```

**Alternative (multipart/form-data):**
```
Content-Type: multipart/form-data

image: [binary file]
```

#### Response

**Success (200):**
```json
{
  "success": true,
  "rooms": [
    {
      "id": "room_001",
      "bounding_box": [100, 200, 500, 600],
      "name_hint": "Kitchen"
    }
  ],
  "processing_time": 12.5,
  "model": "claude-3.5-sonnet"
}
```

**Error (500):**
```json
{
  "success": false,
  "error": "Error message",
  "rooms": []
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether detection succeeded |
| `rooms` | array | List of detected rooms |
| `rooms[].id` | string | Unique room identifier |
| `rooms[].bounding_box` | array | [x_min, y_min, x_max, y_max] normalized 0-1000 |
| `rooms[].name_hint` | string | Room name/type (optional) |
| `processing_time` | float | Processing time in seconds |
| `model` | string | AI model used |
| `error` | string | Error message (if failed) |

#### Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid image format |
| 401 | Unauthorized - Missing/invalid API key |
| 413 | Payload Too Large - Image > 10MB |
| 500 | Internal Server Error |
| 504 | Gateway Timeout - Processing > 60s |

## Example Usage

### cURL
```bash
curl -X POST https://api.example.com/detect-rooms \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "image": "base64_encoded_image",
    "filename": "blueprint.png"
  }'
```

### JavaScript
```javascript
const response = await fetch('https://api.example.com/detect-rooms', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'YOUR_API_KEY'
  },
  body: JSON.stringify({
    image: base64Image,
    filename: 'blueprint.png'
  })
});

const data = await response.json();
console.log(data.rooms);
```

### Python
```python
import requests
import base64

with open('blueprint.png', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    'https://api.example.com/detect-rooms',
    headers={
        'Content-Type': 'application/json',
        'x-api-key': 'YOUR_API_KEY'
    },
    json={
        'image': image_base64,
        'filename': 'blueprint.png'
    }
)

data = response.json()
print(data['rooms'])
```

## Rate Limits

- **Free Tier**: 100 requests/day
- **Paid Tier**: 1000 requests/day
- **Enterprise**: Custom limits

## Support

For issues or questions:
- Email: support@roomvisionai.com
- Documentation: https://docs.roomvisionai.com
- GitHub: https://github.com/sainathyai/RoomVisionAI

