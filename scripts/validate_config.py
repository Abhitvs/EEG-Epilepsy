#!/usr/bin/env python3
"""
Validate the dataset configuration without downloading files.

This script checks if the configuration file is valid and if the Google Drive
file IDs can be extracted properly.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Please install it with: pip install pyyaml")
    sys.exit(1)

from download_datasets import load_config, extract_file_id, validate_config


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description='Validate dataset configuration file.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='configs/datasets.yaml',
        help='Path to the YAML configuration file (default: configs/datasets.yaml)'
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    config_path = project_root / args.config
    
    print("="*60)
    print("Dataset Configuration Validator")
    print("="*60)
    print(f"Configuration file: {config_path}\n")
    
    if not config_path.exists():
        print(f"✗ Configuration file not found: {config_path}")
        sys.exit(1)
    
    config = load_config(config_path)
    if config is None:
        print("✗ Configuration validation failed")
        sys.exit(1)
    
    print("✓ Configuration file is valid\n")
    
    datasets = config.get('datasets', {})
    
    if not datasets:
        print("⚠ No datasets configured")
        sys.exit(0)
    
    print(f"Found {len(datasets)} dataset(s):\n")
    
    all_valid = True
    enabled_count = 0
    
    for dataset_name, dataset_config in datasets.items():
        print(f"Dataset: {dataset_name}")
        print(f"  Enabled: {dataset_config.get('enabled', True)}")
        print(f"  Output filename: {dataset_config.get('output_filename', 'N/A')}")
        
        if not dataset_config.get('enabled', True):
            print(f"  Status: Disabled (will be skipped)\n")
            continue
        
        enabled_count += 1
        
        file_id_or_url = dataset_config.get('file_id', '')
        if not file_id_or_url or not file_id_or_url.strip():
            print(f"  File ID: (empty)")
            print(f"  Status: ✗ No file ID provided\n")
            all_valid = False
            continue
        
        file_id = extract_file_id(file_id_or_url)
        
        if file_id:
            print(f"  File ID/URL: {file_id_or_url[:60]}{'...' if len(file_id_or_url) > 60 else ''}")
            print(f"  Extracted ID: {file_id}")
            print(f"  Status: ✓ Valid\n")
        else:
            print(f"  File ID/URL: {file_id_or_url[:60]}{'...' if len(file_id_or_url) > 60 else ''}")
            print(f"  Status: ✗ Invalid file ID or URL format\n")
            all_valid = False
    
    print("="*60)
    print("Summary")
    print("="*60)
    print(f"Total datasets: {len(datasets)}")
    print(f"Enabled datasets: {enabled_count}")
    
    if all_valid and enabled_count > 0:
        print("\n✓ All enabled datasets have valid configuration!")
        print("\nYou can now run: python scripts/download_datasets.py")
    elif enabled_count == 0:
        print("\n⚠ No datasets are enabled for download")
    else:
        print("\n✗ Some datasets have invalid configuration")
        print("  Please fix the issues above before downloading")
        sys.exit(1)


if __name__ == '__main__':
    main()
