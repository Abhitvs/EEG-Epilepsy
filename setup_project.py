#!/usr/bin/env python3
"""
Project Setup Script for EEG-Epilepsy

This script creates the full directory hierarchy and generates configuration files
for the EEG-Epilepsy project. It is idempotent and safe to run multiple times.

Usage:
    python setup_project.py
"""

import os
import sys
from pathlib import Path


def log_action(action, path, status="created"):
    """Log directory or file creation/existence."""
    status_symbol = "✓" if status == "exists" else "+"
    print(f"[{status_symbol}] {action}: {path}")


def create_directories(base_path):
    """Create the project directory structure."""
    directories = [
        "data/raw/delhi_hospital_mat",
        "data/processed",
        "notebooks",
        "src/loaders",
        "models",
        "tests",
    ]
    
    print("\n=== Creating Directory Structure ===")
    for directory in directories:
        dir_path = base_path / directory
        if dir_path.exists():
            log_action("Directory", directory, "exists")
        else:
            os.makedirs(dir_path, exist_ok=True)
            log_action("Directory", directory, "created")


def create_gitignore(base_path):
    """Create .gitignore file if it doesn't exist."""
    gitignore_path = base_path / ".gitignore"
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints/

# Data files
data/raw/
data/processed/
*.mat
*.csv
*.hdf5
*.h5
*.pkl
*.pickle

# Models
models/*.h5
models/*.pkl
models/*.pt
models/*.pth
models/*.ckpt

# Cache
.cache/
*.cache

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Virtual environments
venv/
ENV/
env/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
"""
    
    print("\n=== Creating Configuration Files ===")
    if gitignore_path.exists():
        log_action("File", ".gitignore", "exists")
    else:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        log_action("File", ".gitignore", "created")


def create_requirements(base_path):
    """Create requirements.txt file if it doesn't exist."""
    requirements_path = base_path / "requirements.txt"
    
    requirements_content = """jupyter>=1.0.0
notebook>=6.4.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
pandas>=1.3.0
seaborn>=0.11.0
"""
    
    if requirements_path.exists():
        log_action("File", "requirements.txt", "exists")
    else:
        with open(requirements_path, "w") as f:
            f.write(requirements_content)
        log_action("File", "requirements.txt", "created")


def create_readme(base_path):
    """Create README.md file if it doesn't exist."""
    readme_path = base_path / "README.md"
    
    readme_content = """# EEG-Epilepsy

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
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
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
"""
    
    if readme_path.exists():
        log_action("File", "README.md", "exists")
    else:
        with open(readme_path, "w") as f:
            f.write(readme_content)
        log_action("File", "README.md", "created")


def create_init_files(base_path):
    """Create __init__.py files for Python packages."""
    init_files = [
        "src/__init__.py",
        "src/loaders/__init__.py",
        "tests/__init__.py",
    ]
    
    print("\n=== Creating Python Package Files ===")
    for init_file in init_files:
        init_path = base_path / init_file
        if init_path.exists():
            log_action("File", init_file, "exists")
        else:
            init_path.touch()
            log_action("File", init_file, "created")


def main():
    """Main function to set up the project structure."""
    print("=" * 60)
    print("EEG-Epilepsy Project Setup")
    print("=" * 60)
    
    # Get the base path (project root)
    base_path = Path(__file__).parent.resolve()
    print(f"\nProject root: {base_path}")
    
    try:
        # Create directory structure
        create_directories(base_path)
        
        # Create configuration files
        create_gitignore(base_path)
        create_requirements(base_path)
        create_readme(base_path)
        
        # Create __init__.py files
        create_init_files(base_path)
        
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create and activate a virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("\n2. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n3. Download datasets to data/raw/ directory")
        print("\n4. Start exploring with Jupyter notebooks:")
        print("   jupyter notebook")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
