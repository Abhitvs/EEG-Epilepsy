"""
Loader utilities for Dataset 1: SNMC Patient-wise EEG data.

This module provides functions to load and process Excel (.xlsx) files from the SNMC dataset.
The dataset contains patient-wise data organized in Excel workbooks with multiple sheets.

Excel File Structure:
- Location: SNMC_dataport/Individual_patients_excel_files/
- Files: 12 patients × 4 books each (Patient1_Book1.xlsx, Patient1_Book2.xlsx, etc.)
- Format: Each Excel file has multiple sheets
- Columns: Time (HH-MM-SS) + 16 bipolar EEG channels
- Header row 1: Column names
- Header row 2: "(HH-MM-SS)" label (should be skipped)
- Data starts from row 3

Seizure Information:
- Patient 1 (ID 363) → Has seizures
- Patient 11 (ID 1306) → Has seizures
- All other patients → No seizures
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import numpy as np


# Seizure mapping for patients
PATIENTS_WITH_SEIZURES = {
    1: 363,   # Patient 1 → ID 363
    11: 1306  # Patient 11 → ID 1306
}

# Expected 16 bipolar EEG channels
EXPECTED_CHANNELS = [
    # Right hemisphere
    'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2',
    'FP2-F8', 'F8-T4', 'T4-T6', 'T6-O2',
    # Left hemisphere
    'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1',
    'FP1-F7', 'F7-T3', 'T3-T5', 'T5-O1'
]


def get_data_path() -> Path:
    """Get the path to the SNMC patient-wise Excel dataset."""
    return Path(__file__).parent.parent.parent / "data" / "raw" / "patient_wise_mat"


def has_seizures(patient_id: int) -> bool:
    """
    Check if a patient has seizures.
    
    Args:
        patient_id: Patient number (1-12)
    
    Returns:
        True if the patient has seizures, False otherwise.
    
    Example:
        >>> has_seizures(1)
        True
        >>> has_seizures(2)
        False
    """
    return patient_id in PATIENTS_WITH_SEIZURES


def get_patient_seizure_id(patient_id: int) -> Optional[int]:
    """
    Get the seizure ID for a patient.
    
    Args:
        patient_id: Patient number (1-12)
    
    Returns:
        Seizure ID if patient has seizures, None otherwise.
    
    Example:
        >>> get_patient_seizure_id(1)
        363
        >>> get_patient_seizure_id(2)
        None
    """
    return PATIENTS_WITH_SEIZURES.get(patient_id)


def list_available_files(data_path: Optional[Union[str, Path]] = None) -> Dict[int, List[str]]:
    """
    List all available Excel files in the SNMC dataset directory.
    
    Args:
        data_path: Path to the data directory. If None, uses default path.
    
    Returns:
        Dictionary mapping patient_id to list of Excel file paths for that patient.
    
    Example:
        >>> files = list_available_files()
        >>> print(f"Patient 1 has {len(files[1])} books")
        Patient 1 has 4 books
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    files = {}
    
    if not data_path.exists():
        return files
    
    # Find all Excel files matching the pattern Patient<N>_Book<M>.xlsx
    for file_path in data_path.glob("Patient*.xlsx"):
        filename = file_path.stem  # e.g., "Patient1_Book1"
        
        try:
            # Extract patient number
            parts = filename.split('_')
            if len(parts) >= 1 and parts[0].startswith('Patient'):
                patient_num_str = parts[0].replace('Patient', '')
                patient_num = int(patient_num_str)
                
                if patient_num not in files:
                    files[patient_num] = []
                
                files[patient_num].append(str(file_path))
        except (ValueError, IndexError):
            continue
    
    # Sort file lists for each patient
    for patient_id in files:
        files[patient_id].sort()
    
    return files


def load_patient_book(
    file_path: Union[str, Path],
    verify: bool = True
) -> Dict[str, pd.DataFrame]:
    """
    Load a single Excel book (all sheets) from the SNMC dataset.
    
    Args:
        file_path: Path to the Excel file.
        verify: Whether to verify the file exists before loading.
    
    Returns:
        Dictionary mapping sheet names to DataFrames. Each DataFrame contains:
        - Time column (HH-MM-SS format)
        - 16 bipolar EEG channels
    
    Raises:
        FileNotFoundError: If the file doesn't exist and verify=True.
        ValueError: If the file cannot be loaded or has unexpected format.
    
    Example:
        >>> sheets = load_patient_book("data/raw/patient_wise_mat/Patient1_Book1.xlsx")
        >>> print(f"Loaded {len(sheets)} sheets")
        >>> first_sheet = list(sheets.values())[0]
        >>> print(f"Shape: {first_sheet.shape}")
    """
    file_path = Path(file_path)
    
    if verify and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(file_path)
        sheets = {}
        
        for sheet_name in excel_file.sheet_names:
            try:
                # Read the sheet, skipping the second header row
                # header=0 means first row is the header
                # skiprows=[1] means skip the second row (0-indexed, so row 1)
                df = pd.read_excel(
                    excel_file,
                    sheet_name=sheet_name,
                    header=0,
                    skiprows=[1]
                )
                
                # Validate that we have expected columns
                if df.shape[1] < 17:  # At least Time + 16 channels
                    print(f"Warning: Sheet '{sheet_name}' in {file_path.name} has only {df.shape[1]} columns")
                
                sheets[sheet_name] = df
                
            except Exception as e:
                print(f"Warning: Could not load sheet '{sheet_name}' from {file_path.name}: {e}")
                continue
        
        return sheets
        
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {str(e)}")


def load_patient_data(
    patient_id: int,
    data_path: Optional[Union[str, Path]] = None,
    books: Optional[List[int]] = None
) -> Dict[str, any]:
    """
    Load all data for a specific patient.
    
    Args:
        patient_id: Patient number (1-12).
        data_path: Path to the data directory. If None, uses default path.
        books: List of book numbers to load (1-4). If None, loads all available books.
    
    Returns:
        Dictionary containing:
        - 'patient_id': Patient number
        - 'seizure_id': Seizure ID if patient has seizures, None otherwise
        - 'has_seizures': Boolean indicating if patient has seizures
        - 'books': Dictionary mapping book number to sheets dictionary
        - 'metadata': Additional metadata about the patient
    
    Raises:
        ValueError: If no data files found for the patient.
    
    Example:
        >>> patient_data = load_patient_data(1)
        >>> print(f"Patient {patient_data['patient_id']}")
        >>> print(f"Has seizures: {patient_data['has_seizures']}")
        >>> print(f"Loaded {len(patient_data['books'])} books")
        >>> 
        >>> # Access specific book and sheet
        >>> book1_sheets = patient_data['books'][1]
        >>> sheet_names = list(book1_sheets.keys())
        >>> first_sheet_data = book1_sheets[sheet_names[0]]
        >>> print(f"First sheet shape: {first_sheet_data.shape}")
    """
    if data_path is None:
        data_path = get_data_path()
    else:
        data_path = Path(data_path)
    
    # List available files for this patient
    all_files = list_available_files(data_path)
    
    if patient_id not in all_files:
        raise ValueError(f"No data files found for patient {patient_id}")
    
    patient_files = all_files[patient_id]
    
    # Filter by book numbers if specified
    if books is not None:
        filtered_files = []
        for book_num in books:
            pattern = f"Patient{patient_id}_Book{book_num}.xlsx"
            matching = [f for f in patient_files if Path(f).name == pattern]
            filtered_files.extend(matching)
        patient_files = filtered_files
    
    if not patient_files:
        raise ValueError(f"No data files found for patient {patient_id} with specified books")
    
    # Load all books
    books_data = {}
    for file_path in patient_files:
        # Extract book number from filename
        filename = Path(file_path).stem
        try:
            book_num_str = filename.split('_Book')[1]
            book_num = int(book_num_str)
        except (IndexError, ValueError):
            print(f"Warning: Could not parse book number from {filename}")
            continue
        
        try:
            sheets = load_patient_book(file_path, verify=True)
            books_data[book_num] = sheets
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load {file_path}: {e}")
            continue
    
    return {
        'patient_id': patient_id,
        'seizure_id': get_patient_seizure_id(patient_id),
        'has_seizures': has_seizures(patient_id),
        'books': books_data,
        'metadata': {
            'num_books': len(books_data),
            'total_sheets': sum(len(sheets) for sheets in books_data.values())
        }
    }


def get_sheet_info(sheet_df: pd.DataFrame) -> Dict[str, any]:
    """
    Extract information about a loaded sheet.
    
    Args:
        sheet_df: DataFrame containing sheet data.
    
    Returns:
        Dictionary with information about the sheet (shape, columns, etc.).
    
    Example:
        >>> patient_data = load_patient_data(1)
        >>> book1_sheets = patient_data['books'][1]
        >>> first_sheet = list(book1_sheets.values())[0]
        >>> info = get_sheet_info(first_sheet)
        >>> print(f"Rows: {info['n_rows']}, Channels: {info['n_channels']}")
    """
    info = {
        'n_rows': len(sheet_df),
        'n_columns': len(sheet_df.columns),
        'columns': list(sheet_df.columns),
        'shape': sheet_df.shape,
    }
    
    # Identify which columns are likely EEG channels
    eeg_channels = [col for col in sheet_df.columns if '-' in str(col)]
    info['n_channels'] = len(eeg_channels)
    info['eeg_channels'] = eeg_channels
    
    # Check if we have time column
    time_cols = [col for col in sheet_df.columns if 'time' in str(col).lower()]
    info['has_time_column'] = len(time_cols) > 0
    if time_cols:
        info['time_column'] = time_cols[0]
    
    return info


def extract_eeg_data(sheet_df: pd.DataFrame) -> Tuple[Optional[pd.Series], pd.DataFrame]:
    """
    Extract time and EEG channel data from a sheet DataFrame.
    
    Args:
        sheet_df: DataFrame containing sheet data.
    
    Returns:
        Tuple of (time_series, eeg_dataframe):
        - time_series: Series containing time data, or None if not found
        - eeg_dataframe: DataFrame containing only EEG channel columns
    
    Example:
        >>> patient_data = load_patient_data(1)
        >>> book1_sheets = patient_data['books'][1]
        >>> first_sheet = list(book1_sheets.values())[0]
        >>> time, eeg = extract_eeg_data(first_sheet)
        >>> print(f"EEG data shape: {eeg.shape}")
        >>> print(f"Channels: {list(eeg.columns)}")
    """
    # Find time column
    time_cols = [col for col in sheet_df.columns if 'time' in str(col).lower()]
    time_series = sheet_df[time_cols[0]] if time_cols else None
    
    # Extract EEG channels (columns with '-' in name, indicating bipolar channels)
    eeg_channels = [col for col in sheet_df.columns if '-' in str(col)]
    eeg_dataframe = sheet_df[eeg_channels]
    
    return time_series, eeg_dataframe


def convert_to_numpy(sheet_df: pd.DataFrame) -> Dict[str, np.ndarray]:
    """
    Convert a sheet DataFrame to numpy arrays.
    
    Args:
        sheet_df: DataFrame containing sheet data.
    
    Returns:
        Dictionary containing:
        - 'time': Time array (if available)
        - 'data': EEG data as numpy array with shape (n_samples, n_channels)
        - 'channels': List of channel names
    
    Example:
        >>> patient_data = load_patient_data(1)
        >>> book1_sheets = patient_data['books'][1]
        >>> first_sheet = list(book1_sheets.values())[0]
        >>> arrays = convert_to_numpy(first_sheet)
        >>> print(f"Data shape: {arrays['data'].shape}")
        >>> print(f"Channels: {arrays['channels']}")
    """
    time_series, eeg_df = extract_eeg_data(sheet_df)
    
    result = {
        'data': eeg_df.to_numpy(),
        'channels': list(eeg_df.columns)
    }
    
    if time_series is not None:
        result['time'] = time_series.to_numpy()
    
    return result
