"""
Test SNMC loader with mock Excel data.

This script creates a mock Excel file to test the SNMC loader functionality.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pandas as pd
from loaders import (
    load_patient_book,
    get_sheet_info,
    extract_eeg_data,
    convert_to_numpy,
)


def create_mock_excel_file(file_path):
    """Create a mock Excel file with the expected SNMC structure."""
    # Expected 16 bipolar EEG channels
    channels = [
        # Right hemisphere
        'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2',
        'FP2-F8', 'F8-T4', 'T4-T6', 'T6-O2',
        # Left hemisphere
        'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1',
        'FP1-F7', 'F7-T3', 'T3-T5', 'T5-O1'
    ]
    
    # Create sample data (100 rows)
    n_samples = 100
    
    # Create time column
    time_data = [f"{i//3600:02d}-{(i%3600)//60:02d}-{i%60:02d}" for i in range(n_samples)]
    
    # Create EEG data
    import numpy as np
    eeg_data = np.random.randn(n_samples, 16) * 100  # Random EEG-like values
    
    # Create DataFrame
    data = {'Time': time_data}
    for i, channel in enumerate(channels):
        data[channel] = eeg_data[:, i]
    
    df = pd.DataFrame(data)
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Sheet 1
        # Add header row
        header_df = pd.DataFrame([list(df.columns)], columns=df.columns)
        # Add second row with (HH-MM-SS) label
        label_row = pd.DataFrame([['(HH-MM-SS)'] + [''] * 16], columns=df.columns)
        
        # Write to sheet
        header_df.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=0)
        label_row.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=1)
        df.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=2)
        
        # Sheet 2 (similar structure)
        df2 = df.copy()
        df2['Time'] = [f"{(i+100)//3600:02d}-{((i+100)%3600)//60:02d}-{(i+100)%60:02d}" for i in range(n_samples)]
        header_df.to_excel(writer, sheet_name='Sheet2', index=False, header=False, startrow=0)
        label_row.to_excel(writer, sheet_name='Sheet2', index=False, header=False, startrow=1)
        df2.to_excel(writer, sheet_name='Sheet2', index=False, header=False, startrow=2)


def test_mock_data():
    """Test SNMC loader with mock data."""
    print("="*60)
    print("Testing SNMC Loader with Mock Data")
    print("="*60)
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create mock Excel file
        mock_file = Path(temp_dir) / "Patient1_Book1.xlsx"
        print(f"\n1. Creating mock Excel file: {mock_file.name}")
        create_mock_excel_file(mock_file)
        print("   ✓ Mock file created successfully")
        
        # Test load_patient_book
        print(f"\n2. Testing load_patient_book...")
        sheets = load_patient_book(mock_file)
        print(f"   ✓ Loaded {len(sheets)} sheets")
        assert len(sheets) == 2, "Expected 2 sheets"
        
        # Test first sheet
        print(f"\n3. Testing sheet structure...")
        first_sheet_name = list(sheets.keys())[0]
        first_sheet = sheets[first_sheet_name]
        print(f"   Sheet: {first_sheet_name}")
        print(f"   Shape: {first_sheet.shape}")
        assert first_sheet.shape[0] == 100, "Expected 100 rows of data"
        assert first_sheet.shape[1] == 17, "Expected 17 columns (Time + 16 channels)"
        print("   ✓ Sheet structure is correct")
        
        # Test get_sheet_info
        print(f"\n4. Testing get_sheet_info...")
        info = get_sheet_info(first_sheet)
        print(f"   Rows: {info['n_rows']}")
        print(f"   EEG Channels: {info['n_channels']}")
        print(f"   Has Time Column: {info['has_time_column']}")
        assert info['n_channels'] == 16, "Expected 16 EEG channels"
        assert info['has_time_column'], "Expected time column"
        print("   ✓ Sheet info extraction works correctly")
        
        # Test extract_eeg_data
        print(f"\n5. Testing extract_eeg_data...")
        time_series, eeg_data = extract_eeg_data(first_sheet)
        print(f"   Time series shape: {time_series.shape}")
        print(f"   EEG data shape: {eeg_data.shape}")
        assert eeg_data.shape[1] == 16, "Expected 16 EEG channels"
        assert len(eeg_data) == 100, "Expected 100 samples"
        print("   ✓ EEG data extraction works correctly")
        
        # Test convert_to_numpy
        print(f"\n6. Testing convert_to_numpy...")
        arrays = convert_to_numpy(first_sheet)
        print(f"   Data array shape: {arrays['data'].shape}")
        print(f"   Channels: {len(arrays['channels'])}")
        assert arrays['data'].shape == (100, 16), "Expected (100, 16) array"
        assert len(arrays['channels']) == 16, "Expected 16 channel names"
        assert 'time' in arrays, "Expected time array"
        print("   ✓ NumPy conversion works correctly")
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary directory")


if __name__ == '__main__':
    test_mock_data()
