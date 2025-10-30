"""
Download EEG datasets from Google Drive.

This script downloads the EEG datasets from Google Drive and organizes them
into the appropriate local directory structure.

Google Drive Structure:
- EEG_Epilepsy Datasets/ → Dataset 3: Delhi Hospital .mat files
- SNMC_dataport/Individual_patients_excel_files/ → Dataset 1: SNMC patient Excel files
- eeg_data.csv → Dataset 2: CSV dataset

Local Directory Structure:
- data/raw/delhi_hospital_mat/ → Delhi Hospital .mat files
- data/raw/patient_wise_mat/ → SNMC patient Excel files (despite name, contains .xlsx)
- data/raw/csv_dataset/ → CSV dataset

Usage:
    python scripts/download_datasets.py
    python scripts/download_datasets.py --dataset snmc
    python scripts/download_datasets.py --dataset delhi
    python scripts/download_datasets.py --dataset csv
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Google Drive folder ID for the main dataset folder
GOOGLE_DRIVE_FOLDER_ID = "1kQtQk94z_MP2HK9J8Wf5is3p-mnlCnEK"

# Dataset mappings: (Google Drive path, Local path)
DATASET_MAPPINGS = {
    'delhi': {
        'gdrive_path': 'EEG_Epilepsy Datasets',  # Note: space and "Datasets" suffix
        'local_path': 'data/raw/delhi_hospital_mat',
        'description': 'Dataset 3: Delhi Hospital EEG data (.mat files)'
    },
    'snmc': {
        'gdrive_path': 'SNMC_dataport/Individual_patients_excel_files',
        'local_path': 'data/raw/patient_wise_mat',  # Historical name kept for compatibility
        'description': 'Dataset 1: SNMC patient-wise Excel files'
    },
    'csv': {
        'gdrive_path': 'eeg_data.csv',  # Note: eeg_data.csv not eeg.csv
        'local_path': 'data/raw/csv_dataset/eeg_data.csv',
        'description': 'Dataset 2: CSV dataset'
    }
}


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def create_directories():
    """Create necessary data directories if they don't exist."""
    project_root = get_project_root()
    
    for dataset_info in DATASET_MAPPINGS.values():
        local_path = project_root / dataset_info['local_path']
        
        # For CSV, create parent directory only
        if str(local_path).endswith('.csv'):
            local_path = local_path.parent
        
        local_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {local_path}")


def check_gdown_installed() -> bool:
    """Check if gdown is installed."""
    try:
        import gdown
        return True
    except ImportError:
        return False


def install_gdown():
    """Install gdown package."""
    import subprocess
    
    print("gdown not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        print("✓ gdown installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install gdown: {e}")
        return False


def download_from_gdrive(folder_id: str, output_path: Path, is_folder: bool = True):
    """
    Download file or folder from Google Drive.
    
    Args:
        folder_id: Google Drive folder/file ID
        output_path: Local path to save the downloaded content
        is_folder: True if downloading a folder, False if downloading a single file
    """
    import gdown
    
    if is_folder:
        # Download entire folder
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        print(f"Downloading folder from: {url}")
        gdown.download_folder(url, output=str(output_path), quiet=False, use_cookies=False)
    else:
        # Download single file
        url = f"https://drive.google.com/uc?id={folder_id}"
        print(f"Downloading file from: {url}")
        gdown.download(url, str(output_path), quiet=False)


def download_dataset(dataset_name: str):
    """
    Download a specific dataset.
    
    Args:
        dataset_name: Name of the dataset ('delhi', 'snmc', or 'csv')
    """
    if dataset_name not in DATASET_MAPPINGS:
        print(f"✗ Unknown dataset: {dataset_name}")
        print(f"  Available datasets: {', '.join(DATASET_MAPPINGS.keys())}")
        return False
    
    dataset_info = DATASET_MAPPINGS[dataset_name]
    project_root = get_project_root()
    local_path = project_root / dataset_info['local_path']
    
    print(f"\n{'='*60}")
    print(f"Downloading: {dataset_info['description']}")
    print(f"Source: {dataset_info['gdrive_path']}")
    print(f"Destination: {local_path}")
    print(f"{'='*60}\n")
    
    # Note: This is a placeholder implementation
    # In practice, you would need to:
    # 1. Use gdown to access the shared folder
    # 2. Navigate to the specific subdirectory
    # 3. Download the files to the local path
    
    # For now, we'll just show instructions
    print("⚠️  Manual Download Required:")
    print(f"   1. Visit: https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}")
    print(f"   2. Navigate to: {dataset_info['gdrive_path']}")
    print(f"   3. Download the contents")
    print(f"   4. Place files in: {local_path}")
    print()
    
    # Create the target directory
    if str(local_path).endswith('.csv'):
        local_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        local_path.mkdir(parents=True, exist_ok=True)
    
    return True


def download_all_datasets():
    """Download all datasets."""
    print("\n" + "="*60)
    print("Downloading All EEG Datasets")
    print("="*60)
    
    for dataset_name in DATASET_MAPPINGS.keys():
        download_dataset(dataset_name)


def list_datasets():
    """List all available datasets."""
    print("\nAvailable Datasets:")
    print("="*60)
    
    for name, info in DATASET_MAPPINGS.items():
        print(f"\n{name}:")
        print(f"  Description: {info['description']}")
        print(f"  Google Drive: {info['gdrive_path']}")
        print(f"  Local Path: {info['local_path']}")


def main():
    """Main function to handle command-line arguments and download datasets."""
    parser = argparse.ArgumentParser(
        description='Download EEG datasets from Google Drive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all datasets
  python scripts/download_datasets.py
  
  # Download specific dataset
  python scripts/download_datasets.py --dataset snmc
  python scripts/download_datasets.py --dataset delhi
  python scripts/download_datasets.py --dataset csv
  
  # List available datasets
  python scripts/download_datasets.py --list
        """
    )
    
    parser.add_argument(
        '--dataset',
        type=str,
        choices=['delhi', 'snmc', 'csv', 'all'],
        default='all',
        help='Specific dataset to download (default: all)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available datasets'
    )
    
    args = parser.parse_args()
    
    # Show dataset list if requested
    if args.list:
        list_datasets()
        return
    
    # Create necessary directories
    print("\nSetting up directories...")
    create_directories()
    
    # Download requested dataset(s)
    if args.dataset == 'all':
        download_all_datasets()
    else:
        download_dataset(args.dataset)
    
    print("\n" + "="*60)
    print("Download Instructions Complete")
    print("="*60)
    print("\nNote: Due to Google Drive's folder structure, manual download may be required.")
    print(f"Main folder: https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}")
    print("\nFor SNMC Excel files:")
    print("  - Navigate to: SNMC_dataport/Individual_patients_excel_files/")
    print("  - Look for files: Patient1_Book1.xlsx, Patient1_Book2.xlsx, etc.")
    print("  - Expected: 12 patients × 4 books = 48 Excel files")


if __name__ == '__main__':
    main()
