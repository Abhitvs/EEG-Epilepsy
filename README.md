# EEG-Epilepsy

EEG analysis project for epilepsy seizure detection and classification.

## Project Overview

This project provides tools and notebooks for analyzing EEG (Electroencephalography) data
to detect and classify epileptic seizures. The project supports multiple datasets and
includes robust data loading utilities, exploratory notebooks, and extensible analysis
pipelines.

## Project Structure

```
EEG-Epilepsy/
├── data/
│   ├── raw/                       # Raw data files (not tracked in git)
│   │   └── delhi_hospital_mat/    # Dataset 3: Delhi Hospital EEG data (.mat files)
│   └── processed/                 # Processed/transformed data (not tracked in git)
├── notebooks/                     # Jupyter notebooks for exploration and analysis
├── src/                          # Source code
│   └── loaders/                  # Data loading utilities
├── models/                       # Trained models (not tracked in git)
├── tests/                        # Unit tests
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── setup_project.py              # This setup script
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- Python >= 3.8
- pip (Python package installer)
- git

### Installation

1. **Clone this repository:**

```bash
git clone <repository-url>
cd EEG-Epilepsy
```

2. **Run the setup script to create the project structure:**

```bash
python setup_project.py
```

This script will:
- Create all necessary directories (data/, notebooks/, src/, models/, tests/)
- Generate configuration files (.gitignore, requirements.txt)
- Be safe to run multiple times (idempotent)

3. **Create and activate a virtual environment (recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Dataset Setup

After setting up the environment, you'll need to download and place the datasets
in the appropriate directories.

**For Dataset 3 (Delhi Hospital):**

Place `.mat` files in `data/raw/delhi_hospital_mat/` directory.

A dataset download script will be provided separately to automate this process.

## Usage

### Exploratory Analysis

Launch Jupyter notebooks to explore the data:

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and open the relevant exploration notebook.

### Programmatic Data Loading

Use the data loader utilities in your Python code:

```python
from src.loaders import load_delhi_segment, list_available_files

# List available data files
files = list_available_files()
print(f"Found {len(files['ictal'])} ictal segments")

# Load a specific segment
segment = load_delhi_segment(files['ictal'][0])
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Features

1. Add source code to appropriate modules in `src/`
2. Add corresponding tests in `tests/`
3. Update documentation as needed
4. Create exploration notebooks in `notebooks/` for new analyses

## Features

- **Robust Data Loading**: Handles various .mat file formats with proper error handling
- **Safeguards**: Graceful handling of missing data files
- **Visualization**: Channel-wise time series plots and spectral analysis
- **Extensible**: Modular design for easy extension

## Dependencies

- **jupyter** >= 1.0.0 - Interactive notebook environment
- **notebook** >= 6.4.0 - Jupyter notebook interface
- **numpy** >= 1.21.0 - Numerical computing
- **scipy** >= 1.7.0 - Scientific computing and signal processing
- **matplotlib** >= 3.4.0 - Plotting and visualization
- **pandas** >= 1.3.0 - Data manipulation and analysis
- **seaborn** >= 0.11.0 - Statistical data visualization

## Contributing

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Ensure all tests pass
5. Submit a pull request

## License

[License information to be added]

## Contact

[Contact information to be added]
