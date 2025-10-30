# Data Loaders Documentation

This document provides comprehensive documentation for the three modular data loaders implemented in this project.

## Overview

The project includes three specialized loaders for different EEG dataset formats:

1. **Dataset 1**: Patient-wise `.mat` files with multiple filter variants
2. **Dataset 2**: CSV datasets with 14 channels plus spectral features
3. **Dataset 3**: Delhi hospital `.mat` files (segmented and labeled)

All loaders follow a consistent API pattern and return data with standardized metadata.

---

## Dataset 1: Patient-wise .mat Files

**Module**: `src/loaders/dataset1_loader.py`

### Key Features

- Loads patient-specific EEG data from `.mat` files
- Supports multiple filter variants (alpha, beta, gamma, delta, theta, raw, filtered)
- Automatically identifies Patient1 and Patient11 as having seizure data
- Extracts patient ID and filter type from filenames
- Provides comprehensive metadata (sampling rate, labels, file origin)

### Main Functions

#### `load_patient_mat(patient_id, filter_type=None, data_path=None, verify=True)`

Loads EEG data for a specific patient.

**Parameters**:
- `patient_id` (str): Patient identifier (e.g., 'Patient1', 'Patient5')
- `filter_type` (str, optional): Filter variant to load (e.g., 'alpha', 'beta')
- `data_path` (Path, optional): Custom data directory path
- `verify` (bool): Whether to verify file exists before loading

**Returns**: Dictionary containing:
- `data`: NumPy array with EEG data (shape: n_channels × n_samples)
- `metadata`: Dict with:
  - `patient_id`: Patient identifier
  - `has_seizure`: Boolean indicating if patient has seizure data
  - `filter_type`: Detected filter type
  - `sampling_rate`: Sampling frequency in Hz
  - `n_channels`: Number of EEG channels
  - `n_samples`: Number of time samples
  - `duration_seconds`: Recording duration
  - `file_origin`: Path to source file
  - `available_filters`: List of available filter types for this patient

**Example**:
```python
from src.loaders import load_patient_mat

data = load_patient_mat('Patient1', filter_type='alpha')
print(f"Shape: {data['data'].shape}")
print(f"Has seizure: {data['metadata']['has_seizure']}")  # True
print(f"Sampling rate: {data['metadata']['sampling_rate']} Hz")
```

#### `list_patient_files(data_path=None)`

Lists all available patient `.mat` files.

**Returns**: Dictionary with patient IDs as keys, each containing a list of file info dicts.

**Example**:
```python
from src.loaders import list_patient_files

files = list_patient_files()
for patient, file_list in files.items():
    print(f"{patient}: {len(file_list)} files")
```

#### `has_seizure_data(patient_id)`

Checks if a patient has seizure data (Patient1 and Patient11 return True).

**Example**:
```python
from src.loaders import has_seizure_data

print(has_seizure_data('Patient1'))   # True
print(has_seizure_data('Patient11'))  # True
print(has_seizure_data('Patient5'))   # False
```

#### Other Utility Functions

- `load_multiple_patients(patient_ids, filter_type=None, data_path=None)`
- `get_patient_info(patient_data)`: Extract summary information
- `identify_patient_from_filename(filename)`: Parse patient ID from filename
- `identify_filter_type(filename)`: Parse filter type from filename

### Data Directory

Place patient `.mat` files in: `data/raw/patient_mat/`

### Filename Conventions

The loader recognizes these patterns:
- Patient ID: `Patient1`, `Patient11`, `P1`, `P11`
- Filter types: `alpha`, `beta`, `gamma`, `delta`, `theta`, `raw`, `filtered`

Examples: `Patient1_alpha.mat`, `P5_beta.mat`

---

## Dataset 2: CSV with Spectral Features

**Module**: `src/loaders/dataset2_loader.py`

### Key Features

- Loads EEG data from CSV files
- Automatically identifies channel columns (14 channels expected)
- Detects spectral feature columns (alpha, beta, delta, theta, gamma power/energy)
- Returns both pandas DataFrame and NumPy arrays
- Infers sampling rate from timestamps or filename

### Main Functions

#### `load_csv_eeg(file_path, verify=True, infer_sampling_rate=True)`

Loads EEG data from a CSV file.

**Parameters**:
- `file_path` (str/Path): Path to the CSV file
- `verify` (bool): Whether to verify file exists
- `infer_sampling_rate` (bool): Try to infer sampling rate from data

**Returns**: Dictionary containing:
- `dataframe`: Complete pandas DataFrame with all columns
- `channels_array`: NumPy array with channel data (n_samples × n_channels)
- `spectral_array`: NumPy array with spectral features (n_samples × n_features)
- `metadata`: Dict with:
  - `sampling_rate`: Sampling frequency in Hz
  - `n_channels`: Number of EEG channels
  - `n_samples`: Number of time samples
  - `channel_columns`: List of channel column names
  - `spectral_columns`: Dict mapping band names to column lists
  - `labels`: Channel labels
  - `file_origin`: Path to source file

**Example**:
```python
from src.loaders import load_csv_eeg

data = load_csv_eeg('eeg_data.csv')
df = data['dataframe']
channels = data['channels_array']  # Shape: (n_samples, 14)
print(f"Channels: {data['metadata']['channel_columns']}")
print(f"Spectral features: {data['metadata']['spectral_columns']}")
```

#### `list_csv_files(data_path=None)`

Lists all available CSV files in the dataset directory.

**Returns**: List of file paths (sorted).

**Example**:
```python
from src.loaders import list_csv_files

files = list_csv_files()
print(f"Found {len(files)} CSV files")
```

#### `concatenate_csv_data(data_list, align_channels=True)`

Concatenates multiple loaded CSV datasets.

**Example**:
```python
from src.loaders import load_multiple_csv_files, concatenate_csv_data

files = list_csv_files()
data_list = load_multiple_csv_files(files[:3])
combined = concatenate_csv_data(data_list)
print(f"Combined shape: {combined['channels_array'].shape}")
```

#### Other Utility Functions

- `load_multiple_csv_files(file_paths, max_files=None)`
- `get_csv_info(csv_data)`: Extract summary information
- `identify_channel_columns(columns)`: Identify EEG channel columns
- `identify_spectral_columns(columns)`: Identify spectral feature columns

### Data Directory

Place CSV files in: `data/raw/csv_eeg/`

### Column Naming Conventions

The loader recognizes:
- **Channels**: `ch1`, `ch2`, ..., `channel_1`, `eeg_1`, or standard electrode names (Fp1, Fp2, F3, F4, etc.)
- **Spectral features**: Columns containing `alpha`, `beta`, `gamma`, `delta`, `theta`, `power`, `energy`, `psd`

### Sampling Rate Detection

The loader attempts to infer sampling rate from:
1. Time/timestamp columns (calculating time differences)
2. Filename patterns (e.g., `data_256hz.csv`)
3. Default: 256 Hz if not found

---

## Dataset 3: Delhi Hospital Segmented Data

**Module**: `src/loaders/dataset3_loader.py`

### Key Features

- Loads segmented `.mat` files from Delhi Hospital dataset
- Automatically identifies segment labels (pre-ictal, interictal, ictal)
- Provides consistent metadata structure
- Default sampling rate: 178 Hz (common for Delhi dataset)

### Main Functions

#### `load_delhi_segment(file_path, verify=True)`

Loads a single `.mat` file segment.

**Parameters**:
- `file_path` (str/Path): Path to the `.mat` file
- `verify` (bool): Whether to verify file exists

**Returns**: Dictionary containing:
- `data`: NumPy array with EEG data (shape: n_channels × n_samples)
- `metadata`: Dict with:
  - `label`: Segment label ('pre_ictal', 'interictal', 'ictal')
  - `sampling_rate`: Sampling frequency in Hz
  - `n_channels`: Number of EEG channels
  - `n_samples`: Number of time samples
  - `duration_seconds`: Segment duration
  - `file_origin`: Path to source file

**Example**:
```python
from src.loaders import load_delhi_segment

data = load_delhi_segment('ictal_segment_01.mat')
print(f"Shape: {data['data'].shape}")
print(f"Label: {data['metadata']['label']}")
print(f"Sampling rate: {data['metadata']['sampling_rate']} Hz")
```

#### `list_available_files(data_path=None)`

Lists all available `.mat` files organized by category.

**Returns**: Dictionary with keys 'pre_ictal', 'interictal', 'ictal'.

**Example**:
```python
from src.loaders import list_available_files

files = list_available_files()
print(f"Pre-ictal: {len(files['pre_ictal'])} files")
print(f"Interictal: {len(files['interictal'])} files")
print(f"Ictal: {len(files['ictal'])} files")
```

#### Other Utility Functions

- `load_multiple_segments(file_paths, max_segments=None)`
- `get_segment_info(segment)`: Extract information about a segment
- `extract_data_array(segment)`: Extract the main data array
- `identify_label_from_filename(filename)`: Parse segment label from filename

### Data Directory

Place Delhi Hospital `.mat` files in: `data/raw/delhi_hospital_mat/`

### Filename Conventions

The loader recognizes these patterns:
- **Pre-ictal**: `preictal`, `pre_ictal`, `pre-ictal`
- **Interictal**: `interictal`, `inter-ictal`
- **Ictal**: `ictal` (without 'pre' prefix)

---

## Common Patterns

### Error Handling

All loaders include:
- **File validation**: Check file existence before loading
- **Format validation**: Verify data structure and format
- **Graceful failures**: Return empty structures for missing files
- **Informative errors**: Clear error messages with context

### Metadata Consistency

All loaders provide:
- `sampling_rate`: Sampling frequency in Hz
- `file_origin`: Path to source file
- `n_channels`: Number of EEG channels
- `n_samples`: Number of time samples
- `duration_seconds`: Recording/segment duration

### Usage in Notebooks and Training Pipelines

```python
# Import all loaders
from src.loaders import (
    load_patient_mat,
    load_csv_eeg,
    load_delhi_segment,
    list_patient_files,
    list_csv_files,
    list_available_files,
)

# List all available data
patient_files = list_patient_files()
csv_files = list_csv_files()
delhi_files = list_available_files()

# Load data as needed
patient_data = load_patient_mat('Patient1') if patient_files else None
csv_data = load_csv_eeg(csv_files[0]) if csv_files else None
delhi_data = load_delhi_segment(delhi_files['ictal'][0]) if delhi_files['ictal'] else None
```

### Testing

Run the test suite:
```bash
python test_loaders.py
```

Run usage examples:
```bash
python examples_usage.py
```

---

## API Reference

All loader functions are exposed through `src/loaders/__init__.py`:

```python
from src.loaders import (
    # Dataset 1
    load_patient_mat,
    load_multiple_patients,
    list_patient_files,
    get_patient_info,
    has_seizure_data,
    identify_patient_from_filename,
    identify_filter_type,
    
    # Dataset 2
    load_csv_eeg,
    load_multiple_csv_files,
    concatenate_csv_data,
    list_csv_files,
    get_csv_info,
    identify_channel_columns,
    identify_spectral_columns,
    
    # Dataset 3
    load_delhi_segment,
    load_multiple_segments,
    list_available_files,
    get_segment_info,
    extract_data_array,
    identify_label_from_filename,
)
```

---

## Notes

- All loaders use `scipy.io.loadmat` for `.mat` files and `pandas` for CSV files
- Data is converted to NumPy arrays for consistency
- Metadata includes sampling rates, labels, and file origins
- All functions include comprehensive docstrings with usage examples
- Error handling gracefully manages missing files
- Default sampling rates are provided when not found in files
