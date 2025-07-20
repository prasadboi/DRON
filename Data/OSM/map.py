import osmnx as ox
import os
import logging
from AWS.s3_utils import S3Manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeoGraph:
    """
    Handles downloading, caching, and loading road network graphs using a hybrid
    local/S3 storage strategy.
    """
    
    def __init__(
        self,
        s3_manager : S3Manager,
        s3_bucket: str = None,
        cache_dir: str = "cache/graphs",
        location: str = None,
        network_type: str = 'drive'
    ):
        self.s3_manager = s3_manager
        self.cache_dir = cache_dir
        self.s3_bucket = s3_bucket
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            logger.info(f"Created local cache directory at {self.cache_dir}")
        
        self.graph = None
        if location:
            self.graph = self.load_graph(location, network_type)
            
    def load_graph(
        self,
        location : str,
        network_type: str = "drive",
    ):
        """
        Gets the road network for a city using a three-tiered approach:
        1. Check the local cache.
        2. If not found, check the S3 bucket.
        3. If not found, download from OSM, upload to S3, and cache locally.
        """
        file_name = f"{location.replace(' ', '_').replace(',', '_')}_{network_type}.graphml"
        local_file_path = os.path.join(self.cache_dir, file_name)
        s3_object_key = f"graphs/{file_name}"
        
        # Checking the local cache
        if os.path.exists(local_file_path):
            logger.info(f"Loading graph from local cache: {local_file_path}")
            return ox.load_graphml(local_file_path)
        # if not found in the local cache, then check the S3 bucket for the graph and download it into the cache directory
        elif self.s3_manager.object_exists(self.s3_bucket, s3_object_key):
            logger.info(f"Loading graph from S3 bucket: {self.s3_bucket}/{s3_object_key}")
            self.s3_manager.download_file(self.s3_bucket, s3_object_key, local_file_path)
            return ox.load_graphml(local_file_path)
        # if not found in the locacl cache or S3 bucket, then download from OSM and upload to S3, and save it to the local file path as well
        else:
            logger.info(f"Graph not found in local cache or S3 bucket. Downloading from OSM: {location}")
            graph = ox.graph_from_place(location, network_type=network_type)
            ox.save_graphml(graph, local_file_path)
            if self.s3_bucket:
                self.s3_manager.upload_file(local_file_path, self.s3_bucket, s3_object_key)
                logger.info(f"Uploaded graph to S3 bucket: {self.s3_bucket}/{s3_object_key}")
            return graph