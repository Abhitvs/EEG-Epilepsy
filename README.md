# EEG-Epilepsy

A machine learning project for analyzing EEG data related to epilepsy detection and classification.

> **Quick Start**: New to this project? Check out the [QUICKSTART.md](QUICKSTART.md) guide for a quick setup tutorial.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
  - [Configuring Google Drive Links](#configuring-google-drive-links)
  - [Downloading Datasets](#downloading-datasets)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

This project provides tools for downloading and processing EEG epilepsy datasets from Google Drive. The datasets are organized into three main categories:

- **patient_wise_mat**: Patient-wise MATLAB format data
- **csv_dataset**: CSV format dataset
- **delhi_hospital_mat**: Delhi hospital MATLAB format data

## Project Structure

```
.
├── configs/
│   └── datasets.yaml          # Configuration file for Google Drive datasets
├── data/
│   └── raw/
│       ├── patient_wise_mat/  # Patient-wise MATLAB data
│       ├── csv_dataset/       # CSV format data
│       └── delhi_hospital_mat/ # Delhi hospital MATLAB data
├── scripts/
│   └── download_datasets.py   # Dataset download script
├── setup_project.py           # Project setup script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for downloading datasets

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd EEG-Epilepsy
```

2. Run the setup script to create directories and install dependencies:

```bash
python setup_project.py
```

This script will:
- Create necessary project directories
- Install required Python packages (gdown, pyyaml)
- Verify configuration files

Alternatively, you can manually install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Configuring Google Drive Links

Before downloading datasets, you need to configure the Google Drive file IDs or URLs in the configuration file.

1. Open `configs/datasets.yaml` in your text editor

2. For each dataset you want to download, add the Google Drive file ID or URL to the `file_id` field

**Supported formats:**

- Full sharing URL: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- Direct URL: `https://drive.google.com/uc?id=FILE_ID`
- File ID only: `FILE_ID`

**Example configuration:**

```yaml
datasets:
  patient_wise_mat:
    file_id: "1a2b3c4d5e6f7g8h9i0j"  # Your Google Drive file ID
    output_filename: "patient_wise_data.mat"
    enabled: true
  
  csv_dataset:
    file_id: "https://drive.google.com/file/d/1x2y3z4a5b6c7d8e9f0g/view?usp=sharing"
    output_filename: "dataset.csv"
    enabled: true
  
  delhi_hospital_mat:
    file_id: ""  # Leave empty to skip this dataset
    output_filename: "delhi_hospital_data.mat"
    enabled: false  # Or set to false to skip
```

**How to get Google Drive file IDs:**

1. Upload your dataset file to Google Drive
2. Right-click the file and select "Get link"
3. Make sure the link sharing is set to "Anyone with the link"
4. Copy the URL - it will look like: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
5. You can paste the entire URL into the `file_id` field, or extract just the FILE_ID portion

### Downloading Datasets

After configuring the Google Drive links, you can validate your configuration first, then run the download script.

#### Validating Configuration (Optional but Recommended)

Before downloading, you can validate your configuration to ensure all file IDs are properly formatted:

```bash
python scripts/validate_config.py
```

This will check if all enabled datasets have valid Google Drive file IDs without actually downloading anything.

#### Basic usage:

```bash
python scripts/download_datasets.py
```

This will download all enabled datasets defined in `configs/datasets.yaml`.

#### Advanced options:

**Download specific datasets only:**

```bash
python scripts/download_datasets.py --datasets patient_wise_mat csv_dataset
```

**Use a custom configuration file:**

```bash
python scripts/download_datasets.py --config path/to/custom_config.yaml
```

**Specify a custom data directory:**

```bash
python scripts/download_datasets.py --data-dir /path/to/data
```

**Enable verbose logging:**

```bash
python scripts/download_datasets.py --verbose
```

**Enable fuzzy download (for Google Drive folders or files requiring additional handling):**

```bash
python scripts/download_datasets.py --fuzzy
```

**View all available options:**

```bash
python scripts/download_datasets.py --help
```

#### What the script does:

1. Reads the configuration file (`configs/datasets.yaml`)
2. Validates the configuration structure
3. Extracts Google Drive file IDs from URLs
4. Creates destination directories if they don't exist
5. Downloads each enabled dataset using `gdown`
6. Reports download status and any errors
7. Provides a summary of successful, skipped, and failed downloads

#### Example output:

```
============================================================
Dataset Download Script
============================================================
Configuration file: /path/to/configs/datasets.yaml
Data directory: /path/to/data/raw

Found 3 dataset(s) to process

------------------------------------------------------------
Processing: patient_wise_mat
------------------------------------------------------------
Downloading patient_wise_mat to data/raw/patient_wise_mat/patient_wise_data.mat
Successfully downloaded patient_wise_mat (1,234,567 bytes)

------------------------------------------------------------
Processing: csv_dataset
------------------------------------------------------------
Skipping csv_dataset: No valid file ID or URL provided

------------------------------------------------------------
Processing: delhi_hospital_mat
------------------------------------------------------------
Skipping delhi_hospital_mat (disabled in configuration)

============================================================
Download Summary
============================================================
Successful downloads: 1
Skipped: 2
Failed: 0
============================================================
```

## Configuration

### datasets.yaml Structure

```yaml
datasets:
  <dataset_name>:
    file_id: "<google_drive_file_id_or_url>"
    output_filename: "<filename_to_save_as>"
    enabled: <true|false>
```

**Fields:**

- `file_id`: Google Drive file ID or URL (required)
- `output_filename`: Name of the file to save locally (required)
- `enabled`: Whether to download this dataset (optional, default: true)

### Environment Variables

You can also use environment variables to override configuration values. The script will look for the following environment variables:

- `DATASETS_CONFIG`: Path to the configuration file (overrides `--config`)
- `DATA_DIR`: Path to the data directory (overrides `--data-dir`)

Example:

```bash
export DATASETS_CONFIG=/path/to/custom_config.yaml
export DATA_DIR=/path/to/custom_data
python scripts/download_datasets.py
```

## Troubleshooting

### "ERROR: gdown is not installed"

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### "Configuration file not found"

Make sure you're running the script from the project root directory, or specify the full path to the configuration file:

```bash
python scripts/download_datasets.py --config /full/path/to/configs/datasets.yaml
```

### "Failed to download dataset"

Common issues:

1. **Invalid file ID**: Make sure the Google Drive file ID is correct
2. **Access permissions**: Ensure the Google Drive file is shared with "Anyone with the link"
3. **Network issues**: Check your internet connection
4. **Large files**: For very large files (>100MB), you may need to use the `--fuzzy` flag

### "File already exists"

The script will prompt you to confirm before overwriting existing files. Type `y` or `yes` to overwrite, or `n` to skip.

### Download speed is slow

This is typically due to Google Drive's download speed limits. The script uses `gdown`, which handles Google Drive's download mechanisms automatically.

### Downloading folders instead of single files

Use the `--fuzzy` flag:

```bash
python scripts/download_datasets.py --fuzzy
```

## License

[Add your license information here]

## Contributors

[Add contributor information here]

## Contact

[Add contact information here]
