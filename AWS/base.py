import boto3
import os
from botocore.exceptions import ClientError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSClient:
    """
    A base class to create Boto3 clients or resources, handling the
    endpoint URL for LocalStack.
    """
    def __init__(self, service_name: str, region_name: str = 'us-east-1'):
        self.service_name = service_name
        self.region_name = region_name
        self.endpoint_url = os.environ.get('LOCALSTACK_ENDPOINT_URL')
        self._client = None
        self._resource = None
        
    @property
    def client(self):
        """Lazy-loads and returns a Boto3 client."""
        if self._client is None:
            logger.info(f"Creating Boto3 client for {self.service_name}...")
            if self.endpoint_url:
                logger.info(f"Using custom endpoint URL: {self.endpoint_url}")
            self._client = boto3.client(
                self.service_name,
                region_name=self.region_name,
                endpoint_url=self.endpoint_url
            )
        return self._client

    @property
    def resource(self):
        """Lazy-loads and returns a Boto3 resource."""
        if self._resource is None:
            logger.info(f"Creating Boto3 resource for {self.service_name}...")
            if self.endpoint_url:
                logger.info(f"Using custom endpoint URL: {self.endpoint_url}")
            self._resource = boto3.resource(
                self.service_name,
                region_name=self.region_name,
                endpoint_url=self.endpoint_url
            )
        return self._resource