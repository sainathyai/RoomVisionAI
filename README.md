# RoomVisionAI 🏗️

**AI-Powered Room Detection from Architectural Blueprints**

Automatically detect and extract room boundaries from architectural blueprints using AWS Bedrock and Claude Vision AI. This project eliminates manual tracing, saving significant time in architectural planning and CAD workflows.

---

## 🎯 Project Overview

RoomVisionAI is an intelligent service that analyzes architectural blueprint images and automatically identifies individual rooms, returning precise bounding box coordinates. Built for the Gauntlet AI Week 4 challenge.

**Key Features:**
- ✨ Automatic room boundary detection
- 🎨 Interactive blueprint visualization
- 🚀 Sub-30 second processing time
- 📊 Accurate coordinate extraction
- 🏷️ Intelligent room labeling
- 🌐 Modern React frontend

---

## 🏛️ Architecture

```
React Frontend → API Gateway → AWS Lambda → AWS Bedrock (Claude Vision)
                                    ↓
                              Response Parser
                                    ↓
                          JSON (Room Coordinates)
```

**Tech Stack:**
- **Backend:** AWS Lambda (Python 3.11), AWS Bedrock, Amazon Textract
- **Frontend:** React 18, Vite, TailwindCSS, React-Konva
- **Infrastructure:** AWS API Gateway, S3, CloudWatch
- **AI Model:** Claude 3.5 Sonnet (Vision)

---

## 📋 Prerequisites

- **AWS Account** with Bedrock access
- **Python 3.11+**
- **Node.js 18+**
- **AWS CLI** configured
- **Git**

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:sainathyai/RoomVisionAI.git
cd RoomVisionAI
```

### 2. Backend Setup

```bash
cd backend/lambda
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Configure AWS

See `docs/AWS_SETUP_GUIDE.md` for detailed instructions.

---

## 📁 Project Structure

```
RoomVisionAI/
├── backend/
│   ├── lambda/                 # AWS Lambda functions
│   │   ├── handler.py         # Main Lambda handler
│   │   ├── bedrock_client.py  # Bedrock API wrapper
│   │   ├── image_processor.py # Image preprocessing
│   │   ├── response_parser.py # LLM response parsing
│   │   ├── validator.py       # Coordinate validation
│   │   └── requirements.txt   # Python dependencies
│   ├── tests/                 # Backend tests
│   └── infrastructure/        # CloudFormation templates
│       ├── cloudformation.yaml
│       └── iam-policies.json
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── BlueprintUploader.jsx
│   │   │   ├── BlueprintCanvas.jsx
│   │   │   └── RoomList.jsx
│   │   ├── services/          # API client
│   │   │   └── api.js
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── data-generation/
│   ├── scripts/               # Synthetic data generation
│   │   ├── blueprint_generator.py
│   │   ├── ground_truth_generator.py
│   │   └── generate_test_suite.py
│   ├── blueprints/            # Generated blueprint images
│   └── ground-truth/          # Expected outputs
│
├── docs/                      # Documentation
│   ├── TECHNICAL_WRITEUP.md
│   ├── AWS_SETUP_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   └── DATA_GENERATION_GUIDE.md
│
├── .gitignore
├── README.md
├── PROJECT_APPROACH.md        # Technical approach
└── IMPLEMENTATION_PLAN.md     # Step-by-step plan
```

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend/lambda
pytest tests/ -v
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

### Validation Pipeline

```bash
cd backend/tests
python validation_pipeline.py
```

---

## 📊 Performance Metrics

- **Processing Time:** < 30 seconds per blueprint
- **Detection Accuracy:** > 80% of rooms detected
- **Coordinate Precision:** IoU > 0.75 for 80% of rooms
- **API Response Time:** < 15 seconds average

---

## 🎨 Sample Usage

### API Request

```bash
curl -X POST https://api.example.com/detect-rooms \
  -H "Content-Type: multipart/form-data" \
  -H "x-api-key: YOUR_API_KEY" \
  -F "image=@blueprint.png"
```

### API Response

```json
{
  "success": true,
  "rooms": [
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
  ],
  "processing_time": 12.5,
  "model": "claude-3.5-sonnet"
}
```

---

## 📖 Documentation

- [**Technical Approach**](PROJECT_APPROACH.md) - Detailed technical strategy
- [**Implementation Plan**](IMPLEMENTATION_PLAN.md) - Phase-by-phase development plan
- [**AWS Setup Guide**](docs/AWS_SETUP_GUIDE.md) - AWS configuration instructions
- [**API Documentation**](docs/API_DOCUMENTATION.md) - API reference
- [**Data Generation Guide**](docs/DATA_GENERATION_GUIDE.md) - Synthetic data creation

---

## 🛠️ Development Roadmap

### ✅ Phase 1: Foundation (Week 1)
- [x] Project setup
- [ ] Synthetic data generation
- [ ] AWS configuration
- [ ] Prompt engineering

### 🔄 Phase 2: Backend (Week 2)
- [ ] Lambda function implementation
- [ ] Bedrock API integration
- [ ] API Gateway setup
- [ ] Validation pipeline

### ⏳ Phase 3: Frontend (Week 3)
- [ ] React app development
- [ ] Blueprint visualization
- [ ] Room editing interface
- [ ] UI polish

### ⏳ Phase 4: Finalization (Week 4)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] Demo video

---

## 🤝 Contributing

This is a Gauntlet AI project. For questions or suggestions:

**Author:** Sainath Yatham  
**GitHub:** [@sainathyai](https://github.com/sainathyai)  
**Project:** Gauntlet AI - Week 4

---

## 📝 License

This project is created for educational purposes as part of the Gauntlet AI program.

---

## 🙏 Acknowledgments

- **Gauntlet AI** for the project challenge
- **Innergy** for the problem statement and requirements
- **AWS Bedrock & Anthropic** for Claude Vision capabilities

---

## 📞 Support

For issues or questions:
1. Check the [documentation](docs/)
2. Review the [implementation plan](IMPLEMENTATION_PLAN.md)
3. Open an issue on GitHub

---

**Built with ❤️ using AWS Bedrock, Claude Vision, and React**

