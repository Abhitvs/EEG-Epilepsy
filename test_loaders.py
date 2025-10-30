"""
Basic tests for the loader utilities to ensure they work correctly.
This is not a full test suite, just sanity checks.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import numpy as np
from loaders import (
    load_delhi_segment,
    load_multiple_segments,
    list_available_files,
    get_segment_info,
)
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


if __name__ == '__main__':
    print("Running basic loader tests...\n")
    
    test_list_available_files()
    test_get_data_path()
    test_get_segment_info()
    test_extract_data_array()
    test_load_multiple_segments_with_empty_list()
    
    print("\n✅ All tests passed!")
