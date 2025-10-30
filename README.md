# EEG-Epilepsy

EEG analysis project for epilepsy seizure detection and classification.

## Project Structure

```
EEG-Epilepsy/
├── data/
│   └── raw/
│       ├── delhi_hospital_mat/    # Dataset 3: Delhi Hospital EEG data (.mat files)
│       ├── patient_wise_mat/      # Dataset 1: SNMC patient Excel files (.xlsx)
│       └── csv_dataset/           # Dataset 2: CSV dataset
├── notebooks/
│   ├── dataset1_snmc_exploration.ipynb    # SNMC dataset exploration
│   └── dataset3_delhi_exploration.ipynb   # Delhi Hospital exploration
├── scripts/
│   └── download_datasets.py       # Download datasets from Google Drive
├── src/
│   └── loaders/
│       ├── __init__.py
│       ├── snmc_excel_loader.py   # Data loading utilities for Dataset 1 (SNMC)
│       └── dataset3_loader.py     # Data loading utilities for Dataset 3 (Delhi)
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

### Dataset 1: SNMC Patient-wise Excel Data

Dataset 1 contains patient-wise EEG recordings in Excel format:
- **Format**: Excel (.xlsx) files with multiple sheets
- **Structure**: 12 patients × 4 books each = 48 files
- **Naming**: Patient1_Book1.xlsx, Patient1_Book2.xlsx, etc.
- **Channels**: 16 bipolar EEG channels (8 right, 8 left hemisphere)
- **Seizure Info**:
  - Patient 1 (ID 363) → Has seizures
  - Patient 11 (ID 1306) → Has seizures
  - All other patients → No seizures

**Data Setup**: Place SNMC Excel files in `data/raw/patient_wise_mat/` directory.

### Dataset 3: Delhi Hospital

Dataset 3 contains EEG recordings in `.mat` format organized into three categories:
- **Pre-ictal**: Recordings before seizure onset
- **Interictal**: Recordings between seizures
- **Ictal**: Recordings during seizures

**Data Setup**: Place Dataset 3 `.mat` files in the `data/raw/delhi_hospital_mat/` directory.

## Downloading Datasets

Use the download script to get the datasets from Google Drive:

```bash
# Download all datasets
python scripts/download_datasets.py

# Download specific dataset
python scripts/download_datasets.py --dataset snmc
python scripts/download_datasets.py --dataset delhi
python scripts/download_datasets.py --dataset csv

# List available datasets
python scripts/download_datasets.py --list
```

## Usage

### Exploratory Analysis

#### SNMC Patient Data (Dataset 1)

To explore the SNMC patient-wise Excel dataset:

```bash
cd notebooks
jupyter notebook dataset1_snmc_exploration.ipynb
```

The notebook demonstrates:
- Loading Excel files with multiple sheets
- Extracting patient metadata (seizure status)
- Accessing time series and EEG channel data
- Converting to NumPy arrays for analysis
- Visualizing EEG signals
- Comparing patients with and without seizures

#### Delhi Hospital Data (Dataset 3)

To explore the Delhi Hospital dataset:

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

#### SNMC Dataset (Excel Files)

```python
from src.loaders import (
    load_patient_book,
    load_patient_data,
    list_available_snmc_files,
    get_sheet_info,
    extract_eeg_data,
    has_seizures,
)

# List available patient files
files = list_available_snmc_files()
print(f"Found {len(files)} patients")

# Check if patient has seizures
print(f"Patient 1 has seizures: {has_seizures(1)}")

# Load all data for a patient (all 4 books)
patient_data = load_patient_data(1)
print(f"Patient {patient_data['patient_id']}: {patient_data['metadata']['num_books']} books")

# Load a single book
book_sheets = load_patient_book("data/raw/patient_wise_mat/Patient1_Book1.xlsx")
print(f"Loaded {len(book_sheets)} sheets")

# Extract EEG data from a sheet
first_sheet = list(book_sheets.values())[0]
time_series, eeg_data = extract_eeg_data(first_sheet)
print(f"EEG data shape: {eeg_data.shape}")
```

#### Delhi Hospital Dataset (.mat Files)

```python
from src.loaders import (
    load_delhi_segment,
    load_multiple_segments,
    list_available_delhi_files,
    get_segment_info,
)

# List available files
files = list_available_delhi_files()
print(f"Found {len(files['ictal'])} ictal segments")

# Load a segment
segment = load_delhi_segment(files['ictal'][0])
print(get_segment_info(segment))

# Load multiple segments
segments = load_multiple_segments(files['pre_ictal'], max_segments=5)
```

## Features

- **Multiple Dataset Support**: 
  - SNMC patient-wise Excel files (.xlsx)
  - Delhi Hospital .mat files
  - CSV dataset
- **Robust Data Loading**: Handles various file formats with proper error handling
- **Seizure Detection Metadata**: Identifies patients with seizures (Patient 1, Patient 11)
- **Safeguards**: Graceful handling of missing data files
- **Visualization**: Channel-wise time series plots and spectral analysis
- **Statistical Analysis**: Basic and spectral statistics computation
- **Extensible**: Clear guidance for adding advanced features

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
- openpyxl >= 3.0.0 (for Excel file support)
