import argparse
import json
import logging
import sys
from AWS.s3_utils import S3Manager
from Data.OSM.map import GeoGraph

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(config_path: str):
    """
    Main function to load configuration and download the city map.
    Args:
        config_path (str): The path to the JSON configuration file.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            logging.info(f"Successfully loaded configuration from {config_path}")
    except FileNotFoundError:
        logging.error(f"Configuration file not found at: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the file: {config_path}")
        sys.exit(1)

    # --- Extract parameters from the configuration ---
    s3_bucket = config.get("s3_bucket")
    location = config.get("location")
    network_type = config.get("network_type", "drive") # Default to 'drive' if not specified
    cache_dir = config.get("cache_dir", "map_cache")  # Default cache directory

    if not s3_bucket or not location:
        logging.error("Configuration must contain 's3_bucket' and 'location' keys.")
        sys.exit(1)

    # --- Initialize utility classes ---
    logging.info("Initializing services...")
    s3_manager = S3Manager()
    graph_loader = GeoGraph(
        s3_manager=s3_manager,
        s3_bucket=s3_bucket,
        cache_dir=cache_dir
    )

    # --- Execute the main logic ---
    logging.info(f"Starting process to get graph for '{location}'...")
    graph = graph_loader.load_graph(
        location=location,
        network_type=network_type
    )

    if graph:
        logging.info(
            f"Successfully loaded graph for '{location}'. "
            f"Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}"
        )
    else:
        logging.error(f"Failed to load graph for '{location}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a city map graph using a configuration file.")
    parser.add_argument(
        "--config_file",
        type=str,
        help="Path to the JSON configuration file."
    )
    args = parser.parse_args()
    main(args.config_file)
