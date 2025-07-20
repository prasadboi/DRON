#!/bin/bash
# init-aws.sh

echo "🚀 Initializing LocalStack resources..."

# Create the S3 bucket for storing data and models
awslocal s3api create-bucket \
  --bucket delivery-optimization-data \
  --region us-east-1

echo "✅ S3 bucket 'delivery-optimization-data' created."

# You can add more commands here, for example, to set up an RDS instance.
# Note: RDS setup can be more complex and might be better handled via your application's startup logic or a separate script.

echo "🎉 LocalStack resources initialized."
