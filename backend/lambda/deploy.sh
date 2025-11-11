#!/bin/bash
# Deployment script for Lambda function

set -e

FUNCTION_NAME="room-detection-handler-dev"
REGION="us-east-1"
ZIP_FILE="function.zip"

echo "Building Lambda deployment package..."

# Create deployment directory
rm -rf package
mkdir -p package

# Install dependencies
pip install -r requirements.txt -t package/

# Copy source code
cp -r ../src package/

# Create handler.py that imports from src
cat > package/handler.py << 'EOF'
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.presentation.lambda.handler import lambda_handler
EOF

# Create zip file
cd package
zip -r ../$ZIP_FILE .
cd ..

echo "Deploying to Lambda..."
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb://$ZIP_FILE \
  --region $REGION

echo "✅ Deployment complete!"
echo "Function: $FUNCTION_NAME"
echo "Region: $REGION"

