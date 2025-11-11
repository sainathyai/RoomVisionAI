# AWS Setup Guide

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Access to AWS Bedrock (may require access request)

## Step 1: Request Bedrock Access

AWS Bedrock requires access approval:

1. Go to AWS Console → Bedrock
2. Click "Request model access"
3. Request access to: **Claude 3.5 Sonnet**
4. Wait for approval (usually 24-48 hours)

## Step 2: Configure IAM Roles

### Lambda Execution Role

Create IAM role for Lambda function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::roomvisionai-blueprints/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "textract:DetectDocumentText"
      ],
      "Resource": "*"
    }
  ]
}
```

### API Gateway Permissions

API Gateway needs permission to invoke Lambda:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:*:*:function:room-detection-handler"
    }
  ]
}
```

## Step 3: Create S3 Bucket

```bash
aws s3 mb s3://roomvisionai-blueprints --region us-east-1
aws s3api put-bucket-versioning \
  --bucket roomvisionai-blueprints \
  --versioning-configuration Status=Enabled
```

## Step 4: Test Bedrock Access

```python
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Test access
try:
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body='{"anthropic_version": "bedrock-2023-05-31", "max_tokens": 10, "messages": [{"role": "user", "content": "test"}]}'
    )
    print("✅ Bedrock access confirmed")
except Exception as e:
    print(f"❌ Bedrock access error: {e}")
```

## Step 5: Environment Variables

Set these in Lambda configuration:

- `BEDROCK_MODEL_ID`: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `BEDROCK_REGION`: `us-east-1`
- `S3_BUCKET`: `roomvisionai-blueprints`
- `LOG_LEVEL`: `INFO`

## Troubleshooting

### Bedrock Access Denied
- Check if model access is approved
- Verify IAM permissions
- Check region (Bedrock may not be available in all regions)

### Lambda Timeout
- Increase timeout to 60 seconds
- Optimize image preprocessing
- Consider async processing for large files

