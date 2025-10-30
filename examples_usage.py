"""
Example usage demonstrations for all three data loaders.

This script shows how to use the data loaders in practical scenarios.
Note: This assumes you have actual data files in the appropriate directories.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from loaders import (
    # Dataset 1
    load_patient_mat,
    list_patient_files,
    has_seizure_data,
    # Dataset 2
    load_csv_eeg,
    list_csv_files,
    concatenate_csv_data,
    # Dataset 3
    load_delhi_segment,
    list_available_files,
)


def example_dataset1():
    """Example usage for Dataset 1: Patient-wise .mat files."""
    print("=== Dataset 1: Patient-wise .mat files ===\n")
    
    # List available patient files
    files = list_patient_files()
    print(f"Found {len(files)} patients")
    
    if not files:
        print("No patient files found. Place .mat files in data/raw/patient_mat/")
        return
    
    # Show available patients
    for patient_id, file_list in files.items():
        has_seizure = has_seizure_data(patient_id)
        print(f"  {patient_id}: {len(file_list)} files (seizure: {has_seizure})")
    
    # Try to load Patient1 if available
    if 'Patient1' in files or any('patient1' in p.lower() for p in files):
        patient_id = 'Patient1' if 'Patient1' in files else [p for p in files if 'patient1' in p.lower()][0]
        try:
            data = load_patient_mat(patient_id)
            print(f"\nLoaded {patient_id}:")
            print(f"  Data shape: {data['data'].shape}")
            print(f"  Sampling rate: {data['metadata']['sampling_rate']} Hz")
            print(f"  Has seizure: {data['metadata']['has_seizure']}")
            print(f"  Filter type: {data['metadata']['filter_type']}")
            print(f"  Duration: {data['metadata']['duration_seconds']:.2f} seconds")
        except Exception as e:
            print(f"Error loading {patient_id}: {e}")
    
    print()


def example_dataset2():
    """Example usage for Dataset 2: CSV with spectral features."""
    print("=== Dataset 2: CSV with spectral features ===\n")
    
    # List available CSV files
    files = list_csv_files()
    print(f"Found {len(files)} CSV files")
    
    if not files:
        print("No CSV files found. Place .csv files in data/raw/csv_eeg/")
        return
    
    # Load first file if available
    try:
        data = load_csv_eeg(files[0])
        print(f"\nLoaded {Path(files[0]).name}:")
        print(f"  Channels: {data['metadata']['n_channels']}")
        print(f"  Samples: {data['metadata']['n_samples']}")
        print(f"  Sampling rate: {data['metadata']['sampling_rate']} Hz")
        print(f"  Duration: {data['metadata'].get('duration_seconds', 'N/A')} seconds")
        print(f"  Channel columns: {data['metadata']['channel_columns']}")
        
        if data['metadata']['spectral_columns']:
            print(f"  Spectral features:")
            for band, cols in data['metadata']['spectral_columns'].items():
                print(f"    {band}: {len(cols)} features")
        
        print(f"\n  DataFrame shape: {data['dataframe'].shape}")
        if data['channels_array'] is not None:
            print(f"  Channels array shape: {data['channels_array'].shape}")
        if data['spectral_array'] is not None:
            print(f"  Spectral array shape: {data['spectral_array'].shape}")
    except Exception as e:
        print(f"Error loading file: {e}")
    
    print()


def example_dataset3():
    """Example usage for Dataset 3: Delhi Hospital."""
    print("=== Dataset 3: Delhi Hospital segmented data ===\n")
    
    # List available files by category
    files = list_available_files()
    print(f"Pre-ictal segments: {len(files['pre_ictal'])}")
    print(f"Interictal segments: {len(files['interictal'])}")
    print(f"Ictal segments: {len(files['ictal'])}")
    
    total = sum(len(v) for v in files.values())
    if total == 0:
        print("\nNo files found. Place .mat files in data/raw/delhi_hospital_mat/")
        return
    
    # Load first available segment
    for label, file_list in files.items():
        if file_list:
            try:
                data = load_delhi_segment(file_list[0])
                print(f"\nLoaded {label} segment:")
                print(f"  File: {Path(file_list[0]).name}")
                print(f"  Data shape: {data['data'].shape}")
                print(f"  Channels: {data['metadata']['n_channels']}")
                print(f"  Samples: {data['metadata']['n_samples']}")
                print(f"  Sampling rate: {data['metadata']['sampling_rate']} Hz")
                print(f"  Duration: {data['metadata']['duration_seconds']:.2f} seconds")
                print(f"  Label: {data['metadata']['label']}")
                break
            except Exception as e:
                print(f"Error loading {label} segment: {e}")
    
    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("EEG Data Loaders - Usage Examples")
    print("=" * 60)
    print()
    
    example_dataset1()
    example_dataset2()
    example_dataset3()
    
    print("=" * 60)
    print("Note: If no files were found, place your data files in:")
    print("  - data/raw/patient_mat/ for Dataset 1")
    print("  - data/raw/csv_eeg/ for Dataset 2")
    print("  - data/raw/delhi_hospital_mat/ for Dataset 3")
    print("=" * 60)


if __name__ == '__main__':
    main()
