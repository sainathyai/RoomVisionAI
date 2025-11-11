# PowerShell deployment script for Lambda function

$FUNCTION_NAME = "room-detection-handler-dev"
$REGION = "us-east-1"
$ZIP_FILE = "function.zip"

Write-Host "Building Lambda deployment package..." -ForegroundColor Green

# Create deployment directory
if (Test-Path "package") {
    Remove-Item -Recurse -Force "package"
}
New-Item -ItemType Directory -Path "package" | Out-Null

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -t package/ --quiet

# Copy source code
Write-Host "Copying source code..." -ForegroundColor Yellow
Copy-Item -Recurse "../src" "package/src"

# Create handler.py
@"
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.presentation.lambda.handler import lambda_handler
"@ | Out-File -FilePath "package/handler.py" -Encoding utf8

# Create zip file
Write-Host "Creating deployment package..." -ForegroundColor Yellow
if (Test-Path $ZIP_FILE) {
    Remove-Item $ZIP_FILE
}

# Use .NET compression for cross-platform compatibility
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory("package", $ZIP_FILE)

Write-Host "Deploying to Lambda..." -ForegroundColor Green
aws lambda update-function-code `
    --function-name $FUNCTION_NAME `
    --zip-file "fileb://$ZIP_FILE" `
    --region $REGION

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment complete!" -ForegroundColor Green
    Write-Host "Function: $FUNCTION_NAME" -ForegroundColor Cyan
    Write-Host "Region: $REGION" -ForegroundColor Cyan
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

