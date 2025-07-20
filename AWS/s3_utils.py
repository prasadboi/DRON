import boto3
import os
from botocore.exceptions import ClientError
import logging
from AWS.base import AWSClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Manager(AWSClient):
    """
    An extensible class for managing S3 operations.
    """
    def __init__(self, region_name: str = 'us-east-1'):
        super().__init__('s3', region_name)

    def object_exists(self, bucket: str, object_name: str) -> bool:
        """
        Check if an object exists in an S3 bucket.
        Args:
            bucket (str): The S3 bucket to check.
            object_name (str): The S3 key (path) of the object.
        Returns:
            bool: True if the object exists, else False.
        """
        try:
            self.client.head_object(Bucket=bucket, Key=object_name)
            return True
        except ClientError as e:
            # If the error code is 404, it means the object does not exist.
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logger.error(f"Error checking object existence: {e}")
                raise

    
    def upload_file(self, file_name: str, bucket: str, object_name: str = None) -> bool:
        """Uploads a file to an S3 bucket."""
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            logger.info(f"Uploading {file_name} to bucket {bucket} as {object_name}...")
            self.client.upload_file(file_name, bucket, object_name)
            logger.info("Upload successful.")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload file: {e}")
            return False
        except FileNotFoundError:
            logger.error(f"The file {file_name} was not found.")
            return False

    def download_file(self, bucket: str, object_name: str, file_name: str) -> bool:
        """Downloads a file from an S3 bucket."""
        try:
            logger.info(f"Downloading s3://{bucket}/{object_name} to {file_name}...")
            self.client.download_file(bucket, object_name, file_name)
            logger.info("Download successful.")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.info(f"File s3://{bucket}/{object_name} not found.")
            else:
                logger.error(f"Failed to download file: {e}")
            return False

    def list_files(self, bucket: str, prefix: str = '') -> list:
        """Lists files in an S3 bucket."""
        try:
            response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            return [item['Key'] for item in response.get('Contents', [])]
        except ClientError as e:
            logger.error(f"Failed to list files in bucket {bucket}: {e}")
            return []