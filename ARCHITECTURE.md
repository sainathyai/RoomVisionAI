# Clean Architecture - RoomVisionAI

## Architecture Overview

This project follows **Clean Architecture** principles to ensure maintainability, testability, and separation of concerns.

## Layer Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  (React Frontend, API Gateway, Lambda Handler)          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Application Layer                       │
│  (Use Cases, Application Services, DTOs)                │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    Domain Layer                          │
│  (Entities, Value Objects, Domain Services)             │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                Infrastructure Layer                      │
│  (AWS Services, File I/O, External APIs)                │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer (Core Business Logic)
**Location:** `backend/src/domain/`

- **Entities:** Core business objects (Room, Blueprint, Wall, etc.)
- **Value Objects:** Immutable objects (Coordinates, BoundingBox, etc.)
- **Domain Services:** Business logic that doesn't belong to a single entity
- **Interfaces:** Contracts for repositories and external services

**Rules:**
- ✅ No dependencies on other layers
- ✅ Pure business logic only
- ✅ Framework-agnostic
- ✅ Highly testable

### 2. Application Layer (Use Cases)
**Location:** `backend/src/application/`

- **Use Cases:** Application-specific business rules
- **DTOs:** Data Transfer Objects for layer communication
- **Interfaces:** Application service contracts
- **Mappers:** Convert between domain entities and DTOs

**Rules:**
- ✅ Depends only on Domain layer
- ✅ Orchestrates domain entities
- ✅ No framework dependencies
- ✅ Defines interfaces for infrastructure

### 3. Infrastructure Layer (External Concerns)
**Location:** `backend/src/infrastructure/`

- **Repositories:** Implement domain repository interfaces
- **AWS Services:** Bedrock client, S3, Lambda handlers
- **File I/O:** Image processing, JSON serialization
- **External APIs:** Third-party service integrations

**Rules:**
- ✅ Implements interfaces from Application/Domain layers
- ✅ Handles all external dependencies
- ✅ Framework-specific code lives here
- ✅ Can depend on Application layer

### 4. Presentation Layer (User Interface)
**Location:** `frontend/` and `backend/src/presentation/`

- **React Components:** UI components
- **API Handlers:** Lambda handler functions
- **Controllers:** Request/response handling
- **View Models:** Data for UI display

**Rules:**
- ✅ Depends on Application layer
- ✅ Handles user input/output
- ✅ No business logic
- ✅ Framework-specific (React, AWS Lambda)

## Dependency Flow

```
Presentation → Application → Domain
     ↓              ↓
Infrastructure → Application → Domain
```

**Key Rule:** Dependencies point inward. Inner layers never depend on outer layers.

## Project Structure

```
backend/
├── src/
│   ├── domain/              # Domain Layer
│   │   ├── entities/
│   │   │   ├── room.py
│   │   │   ├── blueprint.py
│   │   │   └── wall.py
│   │   ├── value_objects/
│   │   │   ├── coordinates.py
│   │   │   └── bounding_box.py
│   │   ├── services/
│   │   │   └── room_detection_service.py
│   │   └── interfaces/
│   │       ├── blueprint_repository.py
│   │       └── vision_service.py
│   │
│   ├── application/         # Application Layer
│   │   ├── use_cases/
│   │   │   ├── detect_rooms.py
│   │   │   └── generate_blueprint.py
│   │   ├── dto/
│   │   │   ├── room_dto.py
│   │   │   └── blueprint_dto.py
│   │   └── mappers/
│   │       └── room_mapper.py
│   │
│   ├── infrastructure/      # Infrastructure Layer
│   │   ├── aws/
│   │   │   ├── bedrock_client.py
│   │   │   └── s3_repository.py
│   │   ├── image/
│   │   │   └── image_processor.py
│   │   └── repositories/
│   │       └── blueprint_repository_impl.py
│   │
│   └── presentation/        # Presentation Layer
│       ├── lambda/
│       │   └── handler.py
│       └── api/
│           └── room_detection_controller.py
│
└── tests/
    ├── unit/               # Unit tests for each layer
    ├── integration/        # Integration tests
    └── e2e/                # End-to-end tests
```

## Testing Strategy

### Unit Tests
- **Domain Layer:** Test entities and value objects in isolation
- **Application Layer:** Mock infrastructure, test use cases
- **Infrastructure Layer:** Mock external services, test adapters

### Integration Tests
- Test layer interactions
- Test AWS service integrations
- Test database/file operations

### E2E Tests
- Test complete user flows
- Test API endpoints
- Test React components

## Benefits of This Architecture

1. **Testability:** Each layer can be tested independently
2. **Maintainability:** Changes in one layer don't affect others
3. **Flexibility:** Easy to swap implementations (e.g., different AI providers)
4. **Scalability:** Clear separation allows parallel development
5. **Framework Independence:** Core logic doesn't depend on AWS/React

## Implementation Guidelines

1. **Start with Domain:** Define entities and value objects first
2. **Define Interfaces:** Create contracts before implementations
3. **Implement Use Cases:** Build application logic using domain entities
4. **Wire Infrastructure:** Implement interfaces with AWS/external services
5. **Connect Presentation:** Build UI/API handlers that use use cases

## Example: Room Detection Flow

```
1. Presentation (Lambda Handler)
   ↓ Receives image upload
   ↓
2. Application (DetectRoomsUseCase)
   ↓ Validates input
   ↓ Calls domain service
   ↓
3. Domain (RoomDetectionService)
   ↓ Defines detection rules
   ↓ Uses VisionService interface
   ↓
4. Infrastructure (BedrockClient)
   ↓ Implements VisionService
   ↓ Calls AWS Bedrock API
   ↓
5. Application (DetectRoomsUseCase)
   ↓ Maps response to domain entities
   ↓
6. Presentation (Lambda Handler)
   ↓ Returns JSON response
```

This ensures business logic remains independent of AWS, making it easy to test and potentially swap AI providers.

