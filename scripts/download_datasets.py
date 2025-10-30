#!/usr/bin/env python3
"""
Download datasets from Google Drive using gdown.

This script reads the configuration from configs/datasets.yaml and downloads
each dataset to the appropriate data/raw/ subdirectory.
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Please install it with: pip install pyyaml")
    sys.exit(1)

try:
    import gdown
except ImportError:
    print("ERROR: gdown is not installed. Please install it with: pip install gdown")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def extract_file_id(file_id_or_url: str) -> Optional[str]:
    """
    Extract Google Drive file ID from various URL formats or return the ID itself.
    
    Args:
        file_id_or_url: Google Drive file ID or URL
    
    Returns:
        Extracted file ID or None if invalid
    """
    if not file_id_or_url or not file_id_or_url.strip():
        return None
    
    file_id_or_url = file_id_or_url.strip()
    
    # Pattern 1: https://drive.google.com/file/d/FILE_ID/view...
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', file_id_or_url)
    if match:
        return match.group(1)
    
    # Pattern 2: https://drive.google.com/uc?id=FILE_ID
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', file_id_or_url)
    if match:
        return match.group(1)
    
    # Pattern 3: https://drive.google.com/open?id=FILE_ID
    match = re.search(r'open\?id=([a-zA-Z0-9_-]+)', file_id_or_url)
    if match:
        return match.group(1)
    
    # If no URL pattern matched, assume it's a file ID
    # Validate that it looks like a file ID (alphanumeric, dash, underscore)
    if re.match(r'^[a-zA-Z0-9_-]+$', file_id_or_url):
        return file_id_or_url
    
    return None


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate the configuration structure.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    if not config:
        logger.error("Configuration is empty")
        return False
    
    if 'datasets' not in config:
        logger.error("Configuration missing 'datasets' key")
        return False
    
    datasets = config['datasets']
    if not isinstance(datasets, dict):
        logger.error("'datasets' must be a dictionary")
        return False
    
    if not datasets:
        logger.warning("No datasets defined in configuration")
        return True
    
    # Validate each dataset entry
    for dataset_name, dataset_config in datasets.items():
        if not isinstance(dataset_config, dict):
            logger.error(f"Dataset '{dataset_name}' configuration must be a dictionary")
            return False
        
        if 'file_id' not in dataset_config:
            logger.error(f"Dataset '{dataset_name}' missing 'file_id' key")
            return False
        
        if 'output_filename' not in dataset_config:
            logger.error(f"Dataset '{dataset_name}' missing 'output_filename' key")
            return False
    
    return True


def load_config(config_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load and validate the YAML configuration file.
    
    Args:
        config_path: Path to the YAML configuration file
    
    Returns:
        Configuration dictionary or None if loading failed
    """
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return None
    
    if not validate_config(config):
        return None
    
    return config


def download_dataset(
    dataset_name: str,
    file_id: str,
    output_path: Path,
    fuzzy: bool = False
) -> bool:
    """
    Download a single dataset from Google Drive.
    
    Args:
        dataset_name: Name of the dataset (for logging)
        file_id: Google Drive file ID
        output_path: Path where the file should be saved
        fuzzy: Whether to use fuzzy download (for folders)
    
    Returns:
        True if download succeeded, False otherwise
    """
    try:
        logger.info(f"Downloading {dataset_name} to {output_path}")
        
        # Create the output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build the Google Drive URL
        url = f"https://drive.google.com/uc?id={file_id}"
        
        # Download the file
        result = gdown.download(url, str(output_path), quiet=False, fuzzy=fuzzy)
        
        if result is None:
            logger.error(f"Failed to download {dataset_name}")
            return False
        
        # Verify the file was created
        if not output_path.exists():
            logger.error(f"Downloaded file not found: {output_path}")
            return False
        
        file_size = output_path.stat().st_size
        logger.info(f"Successfully downloaded {dataset_name} ({file_size:,} bytes)")
        return True
        
    except Exception as e:
        logger.error(f"Error downloading {dataset_name}: {e}")
        return False


def main():
    """Main function to orchestrate dataset downloads."""
    parser = argparse.ArgumentParser(
        description='Download datasets from Google Drive based on configuration.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all enabled datasets
  python scripts/download_datasets.py
  
  # Use a custom configuration file
  python scripts/download_datasets.py --config my_config.yaml
  
  # Enable verbose logging
  python scripts/download_datasets.py --verbose
  
  # Download specific datasets only
  python scripts/download_datasets.py --datasets patient_wise_mat csv_dataset
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='configs/datasets.yaml',
        help='Path to the YAML configuration file (default: configs/datasets.yaml)'
    )
    
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Specific dataset(s) to download (if not specified, all enabled datasets will be downloaded)'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data/raw',
        help='Base directory for data storage (default: data/raw)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--fuzzy',
        action='store_true',
        help='Enable fuzzy download (for Google Drive folders or files requiring additional handling)'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Resolve paths
    project_root = Path(__file__).parent.parent
    config_path = project_root / args.config
    data_dir = project_root / args.data_dir
    
    logger.info("="*60)
    logger.info("Dataset Download Script")
    logger.info("="*60)
    logger.info(f"Configuration file: {config_path}")
    logger.info(f"Data directory: {data_dir}")
    
    # Load configuration
    config = load_config(config_path)
    if config is None:
        logger.error("Failed to load configuration. Exiting.")
        sys.exit(1)
    
    datasets = config.get('datasets', {})
    
    if not datasets:
        logger.warning("No datasets configured. Nothing to download.")
        sys.exit(0)
    
    # Filter datasets if specific ones were requested
    if args.datasets:
        requested = set(args.datasets)
        available = set(datasets.keys())
        missing = requested - available
        
        if missing:
            logger.warning(f"Requested datasets not found in config: {', '.join(missing)}")
        
        datasets = {k: v for k, v in datasets.items() if k in requested}
        
        if not datasets:
            logger.error("None of the requested datasets are available in the configuration.")
            sys.exit(1)
    
    # Process each dataset
    logger.info(f"\nFound {len(datasets)} dataset(s) to process")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for dataset_name, dataset_config in datasets.items():
        logger.info(f"\n{'-'*60}")
        logger.info(f"Processing: {dataset_name}")
        logger.info(f"{'-'*60}")
        
        # Check if dataset is enabled
        if not dataset_config.get('enabled', True):
            logger.info(f"Skipping {dataset_name} (disabled in configuration)")
            skip_count += 1
            continue
        
        # Extract file ID
        file_id_or_url = dataset_config.get('file_id', '')
        file_id = extract_file_id(file_id_or_url)
        
        if not file_id:
            logger.warning(f"Skipping {dataset_name}: No valid file ID or URL provided")
            skip_count += 1
            continue
        
        logger.debug(f"Extracted file ID: {file_id}")
        
        # Get output filename
        output_filename = dataset_config.get('output_filename')
        if not output_filename:
            logger.error(f"Skipping {dataset_name}: No output filename specified")
            fail_count += 1
            continue
        
        # Construct output path
        output_path = data_dir / dataset_name / output_filename
        
        # Check if file already exists
        if output_path.exists():
            file_size = output_path.stat().st_size
            logger.warning(f"File already exists: {output_path} ({file_size:,} bytes)")
            response = input("Overwrite? [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                logger.info(f"Skipping {dataset_name}")
                skip_count += 1
                continue
        
        # Download the dataset
        if download_dataset(dataset_name, file_id, output_path, args.fuzzy):
            success_count += 1
        else:
            fail_count += 1
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("Download Summary")
    logger.info(f"{'='*60}")
    logger.info(f"Successful downloads: {success_count}")
    logger.info(f"Skipped: {skip_count}")
    logger.info(f"Failed: {fail_count}")
    logger.info(f"{'='*60}")
    
    if fail_count > 0:
        logger.error("Some downloads failed. Please check the logs above.")
        sys.exit(1)
    elif success_count == 0:
        logger.warning("No datasets were downloaded.")
        sys.exit(0)
    else:
        logger.info("All downloads completed successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
