# EEG-Epilepsy

EEG analysis project for epilepsy seizure detection and classification.

## Project Structure

```
EEG-Epilepsy/
├── data/
│   └── raw/
│       └── delhi_hospital_mat/    # Dataset 3: Delhi Hospital EEG data (.mat files)
├── notebooks/
│   └── dataset3_delhi_exploration.ipynb  # Exploratory analysis notebook
├── src/
│   └── loaders/
│       ├── __init__.py
│       └── dataset3_loader.py     # Data loading utilities for Dataset 3
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

## Dataset 3: Delhi Hospital

Dataset 3 contains EEG recordings in `.mat` format organized into three categories:
- **Pre-ictal**: Recordings before seizure onset
- **Interictal**: Recordings between seizures
- **Ictal**: Recordings during seizures

### Data Setup

Place Dataset 3 `.mat` files in the `data/raw/delhi_hospital_mat/` directory.

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

```python
from src.loaders import (
    load_delhi_segment,
    load_multiple_segments,
    list_available_files,
    get_segment_info,
)

# List available files
files = list_available_files()
print(f"Found {len(files['ictal'])} ictal segments")

# Load a segment
segment = load_delhi_segment(files['ictal'][0])
print(get_segment_info(segment))

# Load multiple segments
segments = load_multiple_segments(files['pre_ictal'], max_segments=5)
```

## Features

- **Robust Data Loading**: Handles various .mat file formats with proper error handling
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
