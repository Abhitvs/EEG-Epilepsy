"""
Basic tests for the loader utilities to ensure they work correctly.
This is not a full test suite, just sanity checks.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import numpy as np
import pandas as pd
from loaders import (
    # Dataset 1
    list_patient_files,
    has_seizure_data,
    identify_patient_from_filename,
    identify_filter_type,
    get_patient_info,
    # Dataset 2
    list_csv_files,
    identify_channel_columns,
    identify_spectral_columns,
    get_csv_info,
    # Dataset 3
    load_delhi_segment,
    load_multiple_segments,
    list_available_files,
    get_segment_info,
    identify_label_from_filename,
)
from loaders.dataset1_loader import get_data_path as get_patient_data_path
from loaders.dataset2_loader import get_data_path as get_csv_data_path
from loaders.dataset3_loader import extract_data_array, get_data_path


def test_list_available_files():
    """Test listing available files (should handle missing data gracefully)."""
    files = list_available_files()
    assert isinstance(files, dict)
    assert 'pre_ictal' in files
    assert 'interictal' in files
    assert 'ictal' in files
    print("✓ test_list_available_files passed")


def test_get_data_path():
    """Test getting the data path."""
    path = get_data_path()
    assert isinstance(path, Path)
    assert 'delhi_hospital_mat' in str(path)
    print("✓ test_get_data_path passed")


def test_get_segment_info():
    """Test segment info extraction."""
    # Create mock segment
    mock_data = np.random.randn(23, 4097)
    segment = {'data': mock_data}
    
    info = get_segment_info(segment)
    assert 'keys' in info
    assert 'shapes' in info
    assert 'n_channels' in info
    assert 'n_samples' in info
    assert info['n_channels'] == 23
    assert info['n_samples'] == 4097
    print("✓ test_get_segment_info passed")


def test_extract_data_array():
    """Test extracting data array from segment."""
    # Test with 'data' key
    mock_data = np.random.randn(23, 4097)
    segment = {'data': mock_data}
    
    extracted = extract_data_array(segment)
    assert extracted is not None
    assert np.array_equal(extracted, mock_data)
    
    # Test with no valid data
    segment_no_data = {'metadata': 'some info'}
    extracted = extract_data_array(segment_no_data)
    assert extracted is None
    
    print("✓ test_extract_data_array passed")


def test_load_multiple_segments_with_empty_list():
    """Test loading multiple segments with empty file list."""
    segments = load_multiple_segments([])
    assert isinstance(segments, list)
    assert len(segments) == 0
    print("✓ test_load_multiple_segments_with_empty_list passed")


# Dataset 1 tests
def test_list_patient_files():
    """Test listing patient files (should handle missing data gracefully)."""
    files = list_patient_files()
    assert isinstance(files, dict)
    print("✓ test_list_patient_files passed")


def test_has_seizure_data():
    """Test seizure data identification for Patient1 and Patient11."""
    assert has_seizure_data('Patient1') == True
    assert has_seizure_data('Patient11') == True
    assert has_seizure_data('Patient5') == False
    assert has_seizure_data('Patient10') == False
    print("✓ test_has_seizure_data passed")


def test_identify_patient_from_filename():
    """Test patient identification from filenames."""
    assert identify_patient_from_filename('Patient1_alpha.mat') is not None
    assert identify_patient_from_filename('P11_data.mat') is not None
    assert identify_patient_from_filename('no_patient.mat') is None
    print("✓ test_identify_patient_from_filename passed")


def test_identify_filter_type():
    """Test filter type identification from filenames."""
    assert identify_filter_type('Patient1_alpha.mat') == 'alpha'
    assert identify_filter_type('Patient5_beta.mat') == 'beta'
    assert identify_filter_type('Patient1_data.mat') is None
    print("✓ test_identify_filter_type passed")


def test_get_patient_info():
    """Test patient info extraction."""
    mock_data = np.random.randn(23, 240000)
    patient_data = {
        'data': mock_data,
        'metadata': {
            'patient_id': 'Patient1',
            'has_seizure': True,
            'sampling_rate': 173.61,
            'n_channels': 23,
            'n_samples': 240000,
        }
    }
    
    info = get_patient_info(patient_data)
    assert 'patient_id' in info
    assert 'has_seizure' in info
    assert info['data_shape'] == (23, 240000)
    print("✓ test_get_patient_info passed")


def test_get_patient_data_path():
    """Test getting the patient data path."""
    path = get_patient_data_path()
    assert isinstance(path, Path)
    assert 'patient_mat' in str(path)
    print("✓ test_get_patient_data_path passed")


# Dataset 2 tests
def test_list_csv_files():
    """Test listing CSV files (should handle missing data gracefully)."""
    files = list_csv_files()
    assert isinstance(files, list)
    print("✓ test_list_csv_files passed")


def test_identify_channel_columns():
    """Test channel column identification."""
    cols = ['ch1', 'ch2', 'ch3', 'alpha_power', 'beta_power']
    channel_cols = identify_channel_columns(cols)
    assert 'ch1' in channel_cols
    assert 'ch2' in channel_cols
    assert 'alpha_power' not in channel_cols
    print("✓ test_identify_channel_columns passed")


def test_identify_spectral_columns():
    """Test spectral column identification."""
    cols = ['ch1', 'alpha_power', 'beta_power', 'theta_energy']
    spectral_cols = identify_spectral_columns(cols)
    assert 'alpha' in spectral_cols
    assert 'beta' in spectral_cols
    assert 'theta' in spectral_cols
    assert 'alpha_power' in spectral_cols['alpha']
    print("✓ test_identify_spectral_columns passed")


def test_get_csv_info():
    """Test CSV info extraction."""
    mock_channels = np.random.randn(1000, 14)
    mock_df = pd.DataFrame(mock_channels, columns=[f'ch{i}' for i in range(1, 15)])
    
    csv_data = {
        'dataframe': mock_df,
        'channels_array': mock_channels,
        'spectral_array': None,
        'metadata': {
            'n_samples': 1000,
            'n_channels': 14,
            'sampling_rate': 256.0,
        }
    }
    
    info = get_csv_info(csv_data)
    assert 'n_channels' in info
    assert 'n_samples' in info
    assert info['channels_shape'] == (1000, 14)
    print("✓ test_get_csv_info passed")


def test_get_csv_data_path():
    """Test getting the CSV data path."""
    path = get_csv_data_path()
    assert isinstance(path, Path)
    assert 'csv_eeg' in str(path)
    print("✓ test_get_csv_data_path passed")


# Dataset 3 tests
def test_identify_label_from_filename():
    """Test label identification from filenames."""
    assert identify_label_from_filename('preictal_01.mat') == 'pre_ictal'
    assert identify_label_from_filename('interictal_02.mat') == 'interictal'
    assert identify_label_from_filename('ictal_03.mat') == 'ictal'
    print("✓ test_identify_label_from_filename passed")


if __name__ == '__main__':
    print("Running basic loader tests...\n")
    
    print("=== Dataset 3 (Delhi Hospital) Tests ===")
    test_list_available_files()
    test_get_data_path()
    test_get_segment_info()
    test_extract_data_array()
    test_load_multiple_segments_with_empty_list()
    test_identify_label_from_filename()
    
    print("\n=== Dataset 1 (Patient-wise .mat) Tests ===")
    test_list_patient_files()
    test_has_seizure_data()
    test_identify_patient_from_filename()
    test_identify_filter_type()
    test_get_patient_info()
    test_get_patient_data_path()
    
    print("\n=== Dataset 2 (CSV) Tests ===")
    test_list_csv_files()
    test_identify_channel_columns()
    test_identify_spectral_columns()
    test_get_csv_info()
    test_get_csv_data_path()
    
    print("\n✅ All tests passed!")
