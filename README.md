# EEG-Epilepsy

EEG analysis project for epilepsy seizure detection and classification.

## Project Structure

```
EEG-Epilepsy/
├── data/
│   └── raw/
│       ├── patient_mat/           # Dataset 1: Patient-wise .mat files with filter variants
│       ├── csv_eeg/               # Dataset 2: CSV files with channels + spectral features
│       └── delhi_hospital_mat/    # Dataset 3: Delhi Hospital EEG data (.mat files)
├── notebooks/
│   └── dataset3_delhi_exploration.ipynb  # Exploratory analysis notebook
├── src/
│   └── loaders/
│       ├── __init__.py
│       ├── dataset1_loader.py     # Patient-wise .mat loader
│       ├── dataset2_loader.py     # CSV dataset loader
│       └── dataset3_loader.py     # Delhi Hospital loader
├── test_loaders.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd EEG-Epilepsy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Datasets

This project supports three types of EEG datasets:

### Dataset 1: Patient-wise .mat files

Patient-specific EEG recordings with multiple filter variants (alpha, beta, gamma, delta, theta). Special handling for Patient1 and Patient11, which are known to contain seizure data.

**Data Setup**: Place `.mat` files in `data/raw/patient_mat/` directory.

### Dataset 2: CSV with spectral features

CSV files containing 14 EEG channels plus spectral features (power in different frequency bands).

**Data Setup**: Place `.csv` files in `data/raw/csv_eeg/` directory.

### Dataset 3: Delhi Hospital

EEG recordings in `.mat` format organized into three categories:
- **Pre-ictal**: Recordings before seizure onset
- **Interictal**: Recordings between seizures
- **Ictal**: Recordings during seizures

**Data Setup**: Place `.mat` files in `data/raw/delhi_hospital_mat/` directory.

## Usage

### Exploratory Analysis

To explore the Delhi Hospital dataset, open and run the Jupyter notebook:

```bash
cd notebooks
jupyter notebook dataset3_delhi_exploration.ipynb
```

The notebook includes:
- Data loading with safeguards for missing data
- Channel-wise EEG signal visualization
- Basic statistical analysis (mean, variance)
- Spectral band power analysis (delta, theta, alpha, beta, gamma)
- Power spectral density comparisons
- Guidance for extending the exploration

### Programmatic Data Loading

#### Dataset 1: Patient-wise .mat files

```python
from src.loaders import load_patient_mat, list_patient_files, has_seizure_data

# List available patient files
files = list_patient_files()
print(f"Found patients: {list(files.keys())}")

# Load a specific patient's data
data = load_patient_mat('Patient1', filter_type='alpha')
print(f"Sampling rate: {data['metadata']['sampling_rate']} Hz")
print(f"Has seizure: {data['metadata']['has_seizure']}")
print(f"Data shape: {data['data'].shape}")

# Check if patient has seizure data
print(f"Patient1 has seizure: {has_seizure_data('Patient1')}")  # True
print(f"Patient11 has seizure: {has_seizure_data('Patient11')}")  # True
```

#### Dataset 2: CSV with spectral features

```python
from src.loaders import load_csv_eeg, list_csv_files, concatenate_csv_data

# List available CSV files
files = list_csv_files()
print(f"Found {len(files)} CSV files")

# Load a CSV file
data = load_csv_eeg(files[0])
print(f"Channels: {data['metadata']['n_channels']}")
print(f"Samples: {data['metadata']['n_samples']}")
print(f"Channel columns: {data['metadata']['channel_columns']}")
print(f"Spectral features: {data['metadata']['spectral_columns']}")

# Access data as DataFrame
df = data['dataframe']
print(df.head())

# Access raw channels as NumPy array
channels_data = data['channels_array']
print(f"Shape: {channels_data.shape}")  # (n_samples, n_channels)
```

#### Dataset 3: Delhi Hospital

```python
from src.loaders import load_delhi_segment, list_available_files

# List available files by category
files = list_available_files()
print(f"Pre-ictal: {len(files['pre_ictal'])}")
print(f"Interictal: {len(files['interictal'])}")
print(f"Ictal: {len(files['ictal'])}")

# Load a segment
if files['ictal']:
    data = load_delhi_segment(files['ictal'][0])
    print(f"Data shape: {data['data'].shape}")
    print(f"Label: {data['metadata']['label']}")
    print(f"Sampling rate: {data['metadata']['sampling_rate']} Hz")
```

## Features

- **Modular Loaders**: Three separate loaders for different dataset types
- **Consistent API**: All loaders return data with consistent structure and metadata
- **Robust Error Handling**: Graceful handling of missing files and format variations
- **Rich Metadata**: Automatic extraction and attachment of sampling rates, labels, and file origins
- **Flexible Data Access**: Support for both NumPy arrays and Pandas DataFrames
- **Validation**: Built-in validation for file existence and data format
- **Comprehensive Documentation**: Inline docstrings with usage examples
- **Special Features**:
  - **Dataset 1**: Automatic seizure detection for Patient1 and Patient11
  - **Dataset 2**: Automatic channel and spectral feature identification
  - **Dataset 3**: Automatic segment label detection (pre-ictal/interictal/ictal)

## Next Steps

See the exploration notebook for detailed suggestions on:
- Advanced feature extraction
- Data preprocessing and filtering
- Enhanced visualizations
- Statistical analysis
- Machine learning preparation

## Dependencies

- Python >= 3.8
- jupyter >= 1.0.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0
- pandas >= 1.3.0
- seaborn >= 0.11.0
