"""
Loader utilities for Dataset 1: Patient-wise EEG data in .mat format.

This module provides functions to load and process patient-wise .mat files
with multiple filter variants. Special logic is included to identify patients
and mark seizure presence for Patient1 and Patient11.

Usage Example:
    >>> from src.loaders import load_patient_mat, list_patient_files
    >>> 
    >>> # List available patient files
    >>> files = list_patient_files()
    >>> print(f"Found patients: {files.keys()}")
    >>> 
    >>> # Load a specific patient's data
    >>> data = load_patient_mat('Patient1', filter_type='alpha')
    >>> print(f"Sampling rate: {data['metadata']['sampling_rate']} Hz")
    >>> print(f"Has seizure: {data['metadata']['has_seizure']}")
    >>> print(f"Data shape: {data['data'].shape}")
    >>> 
    >>> # Load with auto-detection of filter type
    >>> data = load_patient_mat('Patient5')
    >>> print(f"Available filters: {data['metadata']['available_filters']}")
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

import numpy as np
import scipy.io as sio


def get_data_path() -> Path:
    """
    Get the path to the patient-wise dataset directory.
    
    Returns:
        Path object pointing to the data directory.
    """
    return Path(__file__).parent.parent.parent / "data" / "raw" / "patient_mat"


def identify_patient_from_filename(filename: str) -> Optional[str]:
    """
    Extract patient identifier from filename.
    
    Args:
        filename: Name of the file (e.g., 'Patient1_alpha.mat', 'P1_data.mat')
    
    Returns:
        Patient identifier string (e.g., 'Patient1') or None if not found.
    
    Example:
        >>> identify_patient_from_filename('Patient1_alpha.mat')
        'Patient1'
        >>> identify_patient_from_filename('P11_beta.mat')
        'Patient11'
    """
    # Try multiple patterns
    patterns = [
        r'(Patient\d+)',
        r'P(\d+)',
        r'patient(\d+)',
        r'p(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            patient_num = match.group(1) if 'Patient' in match.group(0) else match.group(1)
            return f"Patient{patient_num}" if not match.group(0).startswith('Patient') else match.group(0)
    
    return None


def identify_filter_type(filename: str) -> Optional[str]:
    """
    Extract filter type from filename.
    
    Args:
        filename: Name of the file.
    
    Returns:
        Filter type string (e.g., 'alpha', 'beta', 'gamma', 'delta', 'theta') or None.
    
    Example:
        >>> identify_filter_type('Patient1_alpha.mat')
        'alpha'
        >>> identify_filter_type('Patient5_bandpass_beta.mat')
        'beta'
    """
    filter_types = ['alpha', 'beta', 'gamma', 'delta', 'theta', 'raw', 'filtered']
    filename_lower = filename.lower()
    
    for filter_type in filter_types:
        if filter_type in filename_lower:
            return filter_type
    
    return None


def has_seizure_data(patient_id: str) -> bool:
    """
    Check if a patient has seizure data based on patient ID.
    
    Patient1 and Patient11 are known to have seizure data.
    
    Args:
        patient_id: Patient identifier (e.g., 'Patient1', 'Patient11')
    
    Returns:
        True if patient has seizure data, False otherwise.
    
    Example:
        >>> has_seizure_data('Patient1')
        True
        >>> has_seizure_data('Patient11')
        True
        >>> has_seizure_data('Patient5')
        False
    """
    # Extract numeric part
    match = re.search(r'\d+', patient_id)
    if match:
        patient_num = int(match.group(0))
        return patient_num in [1, 11]
    return False


def list_patient_files(
    data_path: Optional[Union[str, Path]] = None
) -> Dict[str, List[Dict[str, str]]]:
    """
    List all available patient .mat files in the dataset directory.
    
    Args:
        data_path: Path to the data directory. If None, uses default path.
    
    Returns:
        Dictionary with patient IDs as keys, each containing a list of file info dicts.
        Each file info dict contains 'path', 'filter_type', and 'filename' keys.
    
    Example:
        >>> files = list_patient_files()
        >>> for patient, file_list in files.items():
        ...     print(f"{patient}: {len(file_list)} files")
        Patient1: 5 files
        Patient11: 5 files
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    files = {}
    
    if not data_path.exists():
        return files
    
    for file_path in data_path.glob("*.mat"):
        patient_id = identify_patient_from_filename(file_path.name)
        if patient_id:
            if patient_id not in files:
                files[patient_id] = []
            
            filter_type = identify_filter_type(file_path.name)
            files[patient_id].append({
                'path': str(file_path),
                'filter_type': filter_type,
                'filename': file_path.name,
            })
    
    # Sort files within each patient
    for patient_id in files:
        files[patient_id].sort(key=lambda x: x['filename'])
    
    return files


def load_patient_mat(
    patient_id: str,
    filter_type: Optional[str] = None,
    data_path: Optional[Union[str, Path]] = None,
    verify: bool = True
) -> Dict[str, Union[np.ndarray, Dict]]:
    """
    Load EEG data for a specific patient from .mat file.
    
    Args:
        patient_id: Patient identifier (e.g., 'Patient1', 'Patient5')
        filter_type: Filter variant to load (e.g., 'alpha', 'beta'). 
                     If None, loads the first available file for the patient.
        data_path: Path to the data directory. If None, uses default path.
        verify: Whether to verify the file exists before loading.
    
    Returns:
        Dictionary containing:
            - 'data': NumPy array with EEG data (shape: n_channels x n_samples)
            - 'metadata': Dict with sampling_rate, labels, file_origin, patient_id,
                          has_seizure, filter_type, and other available metadata
            - Additional keys from the .mat file
    
    Raises:
        FileNotFoundError: If no matching file is found and verify=True.
        ValueError: If the file cannot be loaded or has unexpected format.
    
    Example:
        >>> data = load_patient_mat('Patient1', filter_type='alpha')
        >>> print(data['data'].shape)
        (23, 240000)
        >>> print(data['metadata']['sampling_rate'])
        173.61
        >>> print(data['metadata']['has_seizure'])
        True
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    # Find matching file
    if not data_path.exists():
        if verify:
            raise FileNotFoundError(f"Data directory not found: {data_path}")
        return None
    
    matching_files = []
    for file_path in data_path.glob("*.mat"):
        file_patient_id = identify_patient_from_filename(file_path.name)
        if file_patient_id and file_patient_id.lower() == patient_id.lower():
            file_filter_type = identify_filter_type(file_path.name)
            if filter_type is None or file_filter_type == filter_type.lower():
                matching_files.append((file_path, file_filter_type))
    
    if not matching_files:
        if verify:
            raise FileNotFoundError(
                f"No .mat files found for {patient_id}" + 
                (f" with filter type '{filter_type}'" if filter_type else "")
            )
        return None
    
    # Use the first matching file
    file_path, detected_filter = matching_files[0]
    
    try:
        mat_data = sio.loadmat(str(file_path))
        
        # Remove metadata keys that scipy.io.loadmat adds
        clean_data = {k: v for k, v in mat_data.items() if not k.startswith('__')}
        
        # Try to find the main data array
        data_array = None
        if 'data' in clean_data:
            data_array = clean_data['data']
        elif 'eeg' in clean_data:
            data_array = clean_data['eeg']
        elif 'signal' in clean_data:
            data_array = clean_data['signal']
        else:
            # Find the largest 2D array
            for key, value in clean_data.items():
                if isinstance(value, np.ndarray) and len(value.shape) == 2:
                    if data_array is None or value.size > data_array.size:
                        data_array = value
        
        if data_array is None:
            raise ValueError(f"Could not find data array in {file_path}")
        
        # Extract or infer metadata
        metadata = {
            'patient_id': patient_id,
            'has_seizure': has_seizure_data(patient_id),
            'filter_type': detected_filter,
            'file_origin': str(file_path),
            'filename': file_path.name,
            'available_filters': [f['filter_type'] for f in matching_files],
        }
        
        # Try to extract sampling rate
        sampling_rate = None
        for key in ['sampling_rate', 'fs', 'srate', 'freq', 'frequency']:
            if key in clean_data:
                value = clean_data[key]
                if isinstance(value, np.ndarray):
                    sampling_rate = float(value.flat[0])
                else:
                    sampling_rate = float(value)
                break
        
        # Default sampling rate if not found (common EEG sampling rate)
        if sampling_rate is None:
            sampling_rate = 256.0  # Default assumption
        
        metadata['sampling_rate'] = sampling_rate
        
        # Try to extract labels/channels
        labels = None
        for key in ['labels', 'channels', 'channel_names']:
            if key in clean_data:
                labels = clean_data[key]
                break
        
        if labels is not None:
            metadata['labels'] = labels
        
        # Data shape information
        metadata['n_channels'] = data_array.shape[0]
        metadata['n_samples'] = data_array.shape[1] if len(data_array.shape) > 1 else data_array.shape[0]
        metadata['duration_seconds'] = metadata['n_samples'] / sampling_rate
        
        result = {
            'data': data_array,
            'metadata': metadata,
        }
        
        # Add any additional data from the mat file
        for key, value in clean_data.items():
            if key not in ['data', 'eeg', 'signal'] and key not in result:
                result[key] = value
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {str(e)}")


def load_multiple_patients(
    patient_ids: List[str],
    filter_type: Optional[str] = None,
    data_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Dict[str, Union[np.ndarray, Dict]]]:
    """
    Load data for multiple patients.
    
    Args:
        patient_ids: List of patient identifiers.
        filter_type: Filter variant to load. If None, loads first available for each patient.
        data_path: Path to the data directory. If None, uses default path.
    
    Returns:
        Dictionary mapping patient IDs to their loaded data.
    
    Example:
        >>> data = load_multiple_patients(['Patient1', 'Patient11'], filter_type='alpha')
        >>> for patient_id, patient_data in data.items():
        ...     print(f"{patient_id}: {patient_data['data'].shape}")
        Patient1: (23, 240000)
        Patient11: (23, 240000)
    """
    results = {}
    
    for patient_id in patient_ids:
        try:
            data = load_patient_mat(patient_id, filter_type=filter_type, 
                                   data_path=data_path, verify=True)
            results[patient_id] = data
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load {patient_id}: {e}")
            continue
    
    return results


def get_patient_info(patient_data: Dict[str, Union[np.ndarray, Dict]]) -> Dict:
    """
    Extract summary information about loaded patient data.
    
    Args:
        patient_data: Dictionary returned by load_patient_mat().
    
    Returns:
        Dictionary with summary information.
    
    Example:
        >>> data = load_patient_mat('Patient1')
        >>> info = get_patient_info(data)
        >>> print(info['patient_id'], info['has_seizure'])
        Patient1 True
    """
    info = patient_data['metadata'].copy()
    
    if 'data' in patient_data:
        data = patient_data['data']
        info['data_shape'] = data.shape
        info['data_dtype'] = str(data.dtype)
        info['data_range'] = (float(np.min(data)), float(np.max(data)))
        info['data_mean'] = float(np.mean(data))
        info['data_std'] = float(np.std(data))
    
    return info
