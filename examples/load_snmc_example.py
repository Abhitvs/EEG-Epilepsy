"""
Example script demonstrating how to load SNMC patient-wise Excel data.

This script shows basic usage of the SNMC Excel loader.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from loaders import (
    load_patient_book,
    load_patient_data,
    list_available_snmc_files,
    get_sheet_info,
    extract_eeg_data,
    has_seizures,
    get_patient_seizure_id,
)


def main():
    print("="*60)
    print("SNMC Patient-wise Excel Data Loader Example")
    print("="*60)
    
    # List available files
    print("\n1. Listing available patient files...")
    available_files = list_available_snmc_files()
    
    if not available_files:
        print("⚠️  No data files found!")
        print("Please download the SNMC dataset first:")
        print("  python scripts/download_datasets.py --dataset snmc")
        return
    
    print(f"Found {len(available_files)} patients\n")
    
    # Show patient information
    print("2. Patient Information:")
    for patient_id in sorted(available_files.keys()):
        files = available_files[patient_id]
        seizure_status = "HAS SEIZURES" if has_seizures(patient_id) else "No seizures"
        seizure_id = get_patient_seizure_id(patient_id)
        id_info = f" (ID: {seizure_id})" if seizure_id else ""
        print(f"   Patient {patient_id}{id_info}: {len(files)} books - {seizure_status}")
    
    # Load a single book
    print("\n3. Loading Patient 1, Book 1...")
    patient_id = 1
    book_file = available_files[patient_id][0]
    
    try:
        sheets = load_patient_book(book_file)
        print(f"   Loaded {len(sheets)} sheets from {Path(book_file).name}")
        
        # Show first sheet info
        first_sheet_name = list(sheets.keys())[0]
        first_sheet = sheets[first_sheet_name]
        
        print(f"\n4. Examining sheet: {first_sheet_name}")
        info = get_sheet_info(first_sheet)
        print(f"   Rows: {info['n_rows']}")
        print(f"   EEG Channels: {info['n_channels']}")
        print(f"   Has Time Column: {info['has_time_column']}")
        
        # Extract EEG data
        print("\n5. Extracting EEG data...")
        time_series, eeg_data = extract_eeg_data(first_sheet)
        print(f"   EEG data shape: {eeg_data.shape}")
        print(f"   Channels: {list(eeg_data.columns)[:4]}... ({len(eeg_data.columns)} total)")
        
        # Load complete patient data
        print(f"\n6. Loading all books for Patient {patient_id}...")
        patient_data = load_patient_data(patient_id)
        print(f"   Patient ID: {patient_data['patient_id']}")
        print(f"   Seizure ID: {patient_data['seizure_id']}")
        print(f"   Has Seizures: {patient_data['has_seizures']}")
        print(f"   Books loaded: {patient_data['metadata']['num_books']}")
        print(f"   Total sheets: {patient_data['metadata']['total_sheets']}")
        
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60)


if __name__ == '__main__':
    main()
