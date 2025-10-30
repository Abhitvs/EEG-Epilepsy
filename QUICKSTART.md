# Quick Start Guide

This guide will help you get started with downloading datasets for the EEG-Epilepsy project.

## Step 1: Setup the Project

Run the setup script to create directories and install dependencies:

```bash
python setup_project.py
```

## Step 2: Configure Google Drive Links

1. Open `configs/datasets.yaml` in your text editor

2. For each dataset, add your Google Drive file ID or URL:

```yaml
datasets:
  patient_wise_mat:
    file_id: "YOUR_FILE_ID_HERE"  # Replace with your actual file ID
    output_filename: "patient_wise_data.mat"
    enabled: true
```

**How to get your Google Drive file ID:**

1. Upload your dataset to Google Drive
2. Right-click the file → "Get link"
3. Set sharing to "Anyone with the link"
4. Copy the URL (looks like: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`)
5. Paste the entire URL or just the FILE_ID into the configuration

## Step 3: Validate Configuration (Optional)

Check if your configuration is valid:

```bash
python scripts/validate_config.py
```

You should see:
```
✓ Configuration file is valid
✓ All enabled datasets have valid configuration!
```

## Step 4: Download Datasets

Run the download script:

```bash
python scripts/download_datasets.py
```

The script will:
- Validate your configuration
- Create necessary directories
- Download each enabled dataset
- Show progress and report any errors

## Example Output

```
============================================================
Dataset Download Script
============================================================
Configuration file: configs/datasets.yaml
Data directory: data/raw

Found 3 dataset(s) to process

------------------------------------------------------------
Processing: patient_wise_mat
------------------------------------------------------------
Downloading patient_wise_mat to data/raw/patient_wise_mat/patient_wise_data.mat
Successfully downloaded patient_wise_mat (1,234,567 bytes)

============================================================
Download Summary
============================================================
Successful downloads: 1
Skipped: 2
Failed: 0
============================================================
```

## Troubleshooting

### Dependencies not installed?

```bash
pip install -r requirements.txt
```

### Configuration errors?

```bash
python scripts/validate_config.py
```

### Need help?

```bash
python scripts/download_datasets.py --help
```

## Next Steps

After downloading your datasets, you can find them in:
- `data/raw/patient_wise_mat/`
- `data/raw/csv_dataset/`
- `data/raw/delhi_hospital_mat/`

See the main [README.md](README.md) for more detailed information.
