"""
Data loader utilities for EEG datasets.

This package provides modular loader utilities for three dataset types:
    1. Patient-wise .mat files with multiple filter variants (Dataset 1)
    2. CSV datasets with 14 channels plus spectral features (Dataset 2)
    3. Delhi hospital .mat files segmented and labeled (Dataset 3)

All loaders convert data to consistent NumPy/Pandas structures and attach
metadata including sampling rate, labels, and file origin.
"""

# Dataset 1: Patient-wise .mat files
from .dataset1_loader import (
    load_patient_mat,
    load_multiple_patients,
    list_patient_files,
    get_patient_info,
    has_seizure_data,
    identify_patient_from_filename,
    identify_filter_type,
)

# Dataset 2: CSV datasets with spectral features
from .dataset2_loader import (
    load_csv_eeg,
    load_multiple_csv_files,
    concatenate_csv_data,
    list_csv_files,
    get_csv_info,
    identify_channel_columns,
    identify_spectral_columns,
)

# Dataset 3: Delhi Hospital segmented .mat files
from .dataset3_loader import (
    load_delhi_segment,
    load_multiple_segments,
    list_available_files as list_available_delhi_files,
    get_segment_info,
    extract_data_array,
    identify_label_from_filename,
)

from .snmc_excel_loader import (
    load_patient_book,
    load_patient_data,
    list_available_files as list_available_snmc_files,
    get_sheet_info,
    extract_eeg_data,
    convert_to_numpy,
    has_seizures,
    get_patient_seizure_id,
)

__all__ = [
    # Dataset 3: Delhi Hospital
    'load_delhi_segment',
    'load_multiple_segments',
    'list_available_delhi_files',
    'get_segment_info',
    # Dataset 1: SNMC
    'load_patient_book',
    'load_patient_data',
    'list_available_snmc_files',
    'get_sheet_info',
    'extract_eeg_data',
    'convert_to_numpy',
    'has_seizures',
    'get_patient_seizure_id',
]
