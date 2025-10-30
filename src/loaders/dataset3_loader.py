"""
Loader utilities for Dataset 3: Delhi Hospital EEG data.

This module provides functions to load and process .mat files from the Delhi Hospital dataset.
The dataset contains pre-ictal, interictal, and ictal segments.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import scipy.io as sio


def get_data_path() -> Path:
    """Get the path to the Delhi Hospital dataset."""
    return Path(__file__).parent.parent.parent / "data" / "raw" / "delhi_hospital_mat"


def list_available_files(data_path: Optional[Union[str, Path]] = None) -> Dict[str, List[str]]:
    """
    List all available .mat files in the Delhi Hospital dataset directory.
    
    Args:
        data_path: Path to the data directory. If None, uses default path.
    
    Returns:
        Dictionary with keys 'pre_ictal', 'interictal', 'ictal' containing lists of file paths.
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    files = {
        'pre_ictal': [],
        'interictal': [],
        'ictal': [],
    }
    
    if not data_path.exists():
        return files
    
    for file_path in data_path.glob("*.mat"):
        filename = file_path.name.lower()
        if 'preictal' in filename or 'pre_ictal' in filename:
            files['pre_ictal'].append(str(file_path))
        elif 'interictal' in filename:
            files['interictal'].append(str(file_path))
        elif 'ictal' in filename and 'pre' not in filename:
            files['ictal'].append(str(file_path))
    
    for key in files:
        files[key].sort()
    
    return files


def load_delhi_segment(
    file_path: Union[str, Path],
    verify: bool = True
) -> Dict[str, np.ndarray]:
    """
    Load a single .mat file segment from the Delhi Hospital dataset.
    
    Args:
        file_path: Path to the .mat file.
        verify: Whether to verify the file exists before loading.
    
    Returns:
        Dictionary containing the loaded data. The structure depends on the .mat file contents.
        Typically includes 'data' key with shape (n_channels, n_samples).
    
    Raises:
        FileNotFoundError: If the file doesn't exist and verify=True.
        ValueError: If the file cannot be loaded or has unexpected format.
    """
    file_path = Path(file_path)
    
    if verify and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        mat_data = sio.loadmat(str(file_path))
        
        # Remove metadata keys that scipy.io.loadmat adds
        clean_data = {k: v for k, v in mat_data.items() if not k.startswith('__')}
        
        # Try to find the main data array
        if 'data' in clean_data:
            data_array = clean_data['data']
        elif len(clean_data) == 1:
            # If there's only one key, assume it's the data
            data_array = list(clean_data.values())[0]
        else:
            # Return all available keys
            data_array = None
        
        result = clean_data.copy()
        
        # Ensure data is in the result
        if data_array is not None and 'data' not in result:
            result['data'] = data_array
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {str(e)}")


def load_multiple_segments(
    file_paths: List[Union[str, Path]],
    max_segments: Optional[int] = None
) -> List[Dict[str, np.ndarray]]:
    """
    Load multiple segment files.
    
    Args:
        file_paths: List of paths to .mat files.
        max_segments: Maximum number of segments to load. If None, loads all.
    
    Returns:
        List of dictionaries, each containing data from one segment.
    """
    if max_segments is not None:
        file_paths = file_paths[:max_segments]
    
    segments = []
    for file_path in file_paths:
        try:
            segment = load_delhi_segment(file_path, verify=True)
            segments.append(segment)
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load {file_path}: {e}")
            continue
    
    return segments


def get_segment_info(segment: Dict[str, np.ndarray]) -> Dict[str, any]:
    """
    Extract information about a loaded segment.
    
    Args:
        segment: Dictionary containing segment data.
    
    Returns:
        Dictionary with information about the segment (shape, keys, etc.).
    """
    info = {
        'keys': list(segment.keys()),
        'shapes': {k: v.shape if isinstance(v, np.ndarray) else type(v).__name__ 
                   for k, v in segment.items()},
    }
    
    # If 'data' key exists, provide more details
    if 'data' in segment:
        data = segment['data']
        if isinstance(data, np.ndarray):
            info['n_channels'] = data.shape[0] if len(data.shape) >= 1 else 1
            info['n_samples'] = data.shape[1] if len(data.shape) >= 2 else data.shape[0]
            info['dtype'] = str(data.dtype)
            info['data_range'] = (float(np.min(data)), float(np.max(data)))
    
    return info


def extract_data_array(segment: Dict[str, np.ndarray]) -> Optional[np.ndarray]:
    """
    Extract the main data array from a segment dictionary.
    
    Args:
        segment: Dictionary containing segment data.
    
    Returns:
        The data array with shape (n_channels, n_samples), or None if not found.
    """
    if 'data' in segment and isinstance(segment['data'], np.ndarray):
        return segment['data']
    
    # Try to find any 2D array that could be the data
    for value in segment.values():
        if isinstance(value, np.ndarray) and len(value.shape) == 2:
            return value
    
    return None
