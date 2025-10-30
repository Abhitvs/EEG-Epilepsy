"""
Loader utilities for Dataset 2: CSV-based EEG data with spectral features.

This module provides functions to load and process CSV files containing
14 EEG channels plus spectral features (e.g., power in different frequency bands).

Usage Example:
    >>> from src.loaders import load_csv_eeg, list_csv_files
    >>> 
    >>> # List available CSV files
    >>> files = list_csv_files()
    >>> print(f"Found {len(files)} CSV files")
    >>> 
    >>> # Load a specific CSV file
    >>> data = load_csv_eeg(files[0])
    >>> print(f"Channels: {data['metadata']['n_channels']}")
    >>> print(f"Samples: {data['metadata']['n_samples']}")
    >>> print(f"Features: {data['metadata']['feature_columns']}")
    >>> 
    >>> # Access data as DataFrame
    >>> df = data['dataframe']
    >>> print(df.head())
    >>> 
    >>> # Access raw channels as NumPy array
    >>> channels_data = data['channels_array']
    >>> print(channels_data.shape)  # (n_samples, n_channels)
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

import numpy as np
import pandas as pd


def get_data_path() -> Path:
    """
    Get the path to the CSV dataset directory.
    
    Returns:
        Path object pointing to the data directory.
    """
    return Path(__file__).parent.parent.parent / "data" / "raw" / "csv_eeg"


def list_csv_files(
    data_path: Optional[Union[str, Path]] = None
) -> List[str]:
    """
    List all available CSV files in the dataset directory.
    
    Args:
        data_path: Path to the data directory. If None, uses default path.
    
    Returns:
        List of file paths to CSV files, sorted alphabetically.
    
    Example:
        >>> files = list_csv_files()
        >>> print(f"Found {len(files)} CSV files")
        >>> print(files[0])
        /path/to/data/eeg_data_001.csv
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    files = []
    
    if not data_path.exists():
        return files
    
    for file_path in data_path.glob("*.csv"):
        files.append(str(file_path))
    
    files.sort()
    return files


def identify_channel_columns(columns: List[str]) -> List[str]:
    """
    Identify which columns represent EEG channels.
    
    Typically looks for columns named like 'ch1', 'channel_1', 'Ch1', etc.
    or standard EEG electrode names (Fp1, Fp2, F3, F4, etc.).
    
    Args:
        columns: List of column names from the DataFrame.
    
    Returns:
        List of column names that are identified as channel data.
    
    Example:
        >>> cols = ['ch1', 'ch2', 'alpha_power', 'beta_power']
        >>> identify_channel_columns(cols)
        ['ch1', 'ch2']
    """
    channel_cols = []
    
    # Common EEG electrode names
    eeg_electrodes = [
        'Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'Fz',
        'C3', 'C4', 'Cz', 'T3', 'T4', 'T5', 'T6',
        'P3', 'P4', 'Pz', 'O1', 'O2', 'Oz',
        'A1', 'A2', 'M1', 'M2',
    ]
    
    for col in columns:
        col_lower = col.lower()
        
        # Check for standard electrode names
        if any(electrode.lower() == col_lower for electrode in eeg_electrodes):
            channel_cols.append(col)
        # Check for channel patterns
        elif re.match(r'^ch\d+$', col_lower) or \
             re.match(r'^channel[\s_-]*\d+$', col_lower) or \
             re.match(r'^eeg[\s_-]*\d+$', col_lower):
            channel_cols.append(col)
    
    return channel_cols


def identify_spectral_columns(columns: List[str]) -> Dict[str, List[str]]:
    """
    Identify which columns represent spectral features.
    
    Looks for columns containing frequency band names (delta, theta, alpha, beta, gamma)
    and feature types (power, amplitude, energy, etc.).
    
    Args:
        columns: List of column names from the DataFrame.
    
    Returns:
        Dictionary mapping feature types to lists of column names.
    
    Example:
        >>> cols = ['ch1', 'alpha_power', 'beta_power', 'theta_energy']
        >>> identify_spectral_columns(cols)
        {'alpha': ['alpha_power'], 'beta': ['beta_power'], 'theta': ['theta_energy']}
    """
    spectral_cols = {
        'delta': [],
        'theta': [],
        'alpha': [],
        'beta': [],
        'gamma': [],
        'other': [],
    }
    
    for col in columns:
        col_lower = col.lower()
        
        # Check for frequency bands
        matched = False
        for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
            if band in col_lower:
                spectral_cols[band].append(col)
                matched = True
                break
        
        # Check for other spectral features
        if not matched:
            spectral_keywords = ['power', 'amplitude', 'energy', 'frequency', 'psd', 'spectral']
            if any(keyword in col_lower for keyword in spectral_keywords):
                spectral_cols['other'].append(col)
    
    # Remove empty categories
    spectral_cols = {k: v for k, v in spectral_cols.items() if v}
    
    return spectral_cols


def load_csv_eeg(
    file_path: Union[str, Path],
    verify: bool = True,
    infer_sampling_rate: bool = True
) -> Dict[str, Union[pd.DataFrame, np.ndarray, Dict]]:
    """
    Load EEG data from a CSV file.
    
    Args:
        file_path: Path to the CSV file.
        verify: Whether to verify the file exists before loading.
        infer_sampling_rate: Whether to try to infer sampling rate from timestamps.
    
    Returns:
        Dictionary containing:
            - 'dataframe': Complete pandas DataFrame with all columns
            - 'channels_array': NumPy array with just the channel data (n_samples, n_channels)
            - 'spectral_array': NumPy array with spectral features (n_samples, n_features) or None
            - 'metadata': Dict with sampling_rate, labels, file_origin, n_channels,
                          n_samples, channel_columns, spectral_columns, etc.
    
    Raises:
        FileNotFoundError: If the file doesn't exist and verify=True.
        ValueError: If the file cannot be loaded or has unexpected format.
    
    Example:
        >>> data = load_csv_eeg('eeg_data.csv')
        >>> print(data['channels_array'].shape)
        (10000, 14)
        >>> print(data['metadata']['sampling_rate'])
        256.0
        >>> print(data['metadata']['channel_columns'])
        ['ch1', 'ch2', ..., 'ch14']
    """
    file_path = Path(file_path)
    
    if verify and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Load CSV file
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError(f"CSV file is empty: {file_path}")
        
        # Identify column types
        columns = df.columns.tolist()
        channel_cols = identify_channel_columns(columns)
        spectral_cols = identify_spectral_columns(columns)
        
        # If no channels identified, try to use first N numeric columns
        if not channel_cols:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # Assume first 14 columns are channels if we have at least that many
            if len(numeric_cols) >= 14:
                channel_cols = numeric_cols[:14]
            else:
                channel_cols = numeric_cols
        
        # Get all spectral feature columns
        all_spectral_cols = []
        for band_cols in spectral_cols.values():
            all_spectral_cols.extend(band_cols)
        
        # Extract arrays
        if channel_cols:
            channels_array = df[channel_cols].to_numpy()
        else:
            channels_array = None
        
        if all_spectral_cols:
            spectral_array = df[all_spectral_cols].to_numpy()
        else:
            spectral_array = None
        
        # Try to infer sampling rate
        sampling_rate = None
        
        # Check if there's a time or timestamp column
        time_cols = [col for col in columns if 'time' in col.lower() or 'timestamp' in col.lower()]
        if time_cols and infer_sampling_rate:
            time_col = time_cols[0]
            if len(df) > 1:
                time_diff = df[time_col].iloc[1] - df[time_col].iloc[0]
                if time_diff > 0:
                    sampling_rate = 1.0 / time_diff
        
        # Check for explicit sampling rate column or in filename
        if sampling_rate is None:
            rate_match = re.search(r'(\d+)hz', file_path.name.lower())
            if rate_match:
                sampling_rate = float(rate_match.group(1))
        
        # Default to common EEG sampling rate
        if sampling_rate is None:
            sampling_rate = 256.0
        
        # Build metadata
        metadata = {
            'file_origin': str(file_path),
            'filename': file_path.name,
            'sampling_rate': sampling_rate,
            'n_samples': len(df),
            'n_channels': len(channel_cols),
            'channel_columns': channel_cols,
            'spectral_columns': spectral_cols,
            'all_columns': columns,
            'n_spectral_features': len(all_spectral_cols),
        }
        
        if channel_cols:
            metadata['labels'] = channel_cols
            metadata['duration_seconds'] = len(df) / sampling_rate
        
        result = {
            'dataframe': df,
            'channels_array': channels_array,
            'spectral_array': spectral_array,
            'metadata': metadata,
        }
        
        return result
        
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty or invalid: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {str(e)}")


def load_multiple_csv_files(
    file_paths: List[Union[str, Path]],
    max_files: Optional[int] = None
) -> List[Dict[str, Union[pd.DataFrame, np.ndarray, Dict]]]:
    """
    Load multiple CSV files.
    
    Args:
        file_paths: List of paths to CSV files.
        max_files: Maximum number of files to load. If None, loads all.
    
    Returns:
        List of dictionaries, each containing data from one file.
    
    Example:
        >>> files = list_csv_files()
        >>> data_list = load_multiple_csv_files(files, max_files=5)
        >>> for i, data in enumerate(data_list):
        ...     print(f"File {i}: {data['metadata']['n_samples']} samples")
    """
    if max_files is not None:
        file_paths = file_paths[:max_files]
    
    results = []
    for file_path in file_paths:
        try:
            data = load_csv_eeg(file_path, verify=True)
            results.append(data)
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load {file_path}: {e}")
            continue
    
    return results


def concatenate_csv_data(
    data_list: List[Dict[str, Union[pd.DataFrame, np.ndarray, Dict]]],
    align_channels: bool = True
) -> Dict[str, Union[pd.DataFrame, np.ndarray, Dict]]:
    """
    Concatenate multiple loaded CSV datasets.
    
    Args:
        data_list: List of data dictionaries from load_csv_eeg().
        align_channels: Whether to ensure all datasets have the same channels.
    
    Returns:
        Dictionary with concatenated data and combined metadata.
    
    Raises:
        ValueError: If datasets cannot be concatenated (e.g., different channels).
    
    Example:
        >>> files = list_csv_files()
        >>> data_list = load_multiple_csv_files(files[:3])
        >>> combined = concatenate_csv_data(data_list)
        >>> print(combined['channels_array'].shape)
        (30000, 14)  # 3 files x 10000 samples each
    """
    if not data_list:
        raise ValueError("data_list is empty")
    
    if align_channels:
        # Check that all have the same channels
        reference_channels = data_list[0]['metadata']['channel_columns']
        for i, data in enumerate(data_list[1:], 1):
            if data['metadata']['channel_columns'] != reference_channels:
                raise ValueError(
                    f"Channel mismatch: file 0 has {reference_channels}, "
                    f"file {i} has {data['metadata']['channel_columns']}"
                )
    
    # Concatenate dataframes
    combined_df = pd.concat([data['dataframe'] for data in data_list], 
                           ignore_index=True)
    
    # Concatenate arrays
    channels_arrays = [data['channels_array'] for data in data_list 
                       if data['channels_array'] is not None]
    combined_channels = np.vstack(channels_arrays) if channels_arrays else None
    
    spectral_arrays = [data['spectral_array'] for data in data_list 
                       if data['spectral_array'] is not None]
    combined_spectral = np.vstack(spectral_arrays) if spectral_arrays else None
    
    # Combine metadata
    file_origins = [data['metadata']['file_origin'] for data in data_list]
    metadata = data_list[0]['metadata'].copy()
    metadata['file_origin'] = file_origins
    metadata['n_samples'] = len(combined_df)
    metadata['n_files'] = len(data_list)
    if 'duration_seconds' in metadata:
        metadata['duration_seconds'] = metadata['n_samples'] / metadata['sampling_rate']
    
    return {
        'dataframe': combined_df,
        'channels_array': combined_channels,
        'spectral_array': combined_spectral,
        'metadata': metadata,
    }


def get_csv_info(csv_data: Dict[str, Union[pd.DataFrame, np.ndarray, Dict]]) -> Dict:
    """
    Extract summary information about loaded CSV data.
    
    Args:
        csv_data: Dictionary returned by load_csv_eeg().
    
    Returns:
        Dictionary with summary information.
    
    Example:
        >>> data = load_csv_eeg('eeg_data.csv')
        >>> info = get_csv_info(data)
        >>> print(info)
        {'n_channels': 14, 'n_samples': 10000, 'sampling_rate': 256.0, ...}
    """
    info = csv_data['metadata'].copy()
    
    if csv_data['channels_array'] is not None:
        data = csv_data['channels_array']
        info['channels_shape'] = data.shape
        info['channels_dtype'] = str(data.dtype)
        info['channels_range'] = (float(np.min(data)), float(np.max(data)))
        info['channels_mean'] = float(np.mean(data))
        info['channels_std'] = float(np.std(data))
    
    if csv_data['spectral_array'] is not None:
        spectral = csv_data['spectral_array']
        info['spectral_shape'] = spectral.shape
        info['spectral_dtype'] = str(spectral.dtype)
    
    return info
