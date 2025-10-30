"""Data loader utilities for EEG datasets"""

from .dataset3_loader import (
    load_delhi_segment,
    load_multiple_segments,
    list_available_files as list_available_delhi_files,
    get_segment_info,
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
