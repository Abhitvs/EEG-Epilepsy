#!/usr/bin/env python3
"""
Project setup script for EEG-Epilepsy.

This script sets up the project environment by creating necessary directories
and installing required dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path


def create_directories():
    """Create necessary project directories."""
    directories = [
        'data/raw/patient_wise_mat',
        'data/raw/csv_dataset',
        'data/raw/delhi_hospital_mat',
        'data/processed',
        'configs',
        'scripts',
        'models',
        'notebooks',
        'logs'
    ]
    
    print("Creating project directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("\nDirectories created successfully!")


def install_dependencies():
    """Install Python dependencies from requirements.txt."""
    requirements_file = Path('requirements.txt')
    
    if not requirements_file.exists():
        print("\nNo requirements.txt found. Skipping dependency installation.")
        return
    
    print("\nInstalling dependencies from requirements.txt...")
    
    pip_commands = [
        [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)],
        [sys.executable, '-m', 'pip', 'install', '--user', '-r', str(requirements_file)],
        [sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-r', str(requirements_file)]
    ]
    
    success = False
    for i, cmd in enumerate(pip_commands):
        try:
            subprocess.check_call(cmd, stderr=subprocess.DEVNULL)
            print("\n✓ Dependencies installed successfully!")
            success = True
            break
        except subprocess.CalledProcessError:
            if i < len(pip_commands) - 1:
                continue
    
    if not success:
        print("\n⚠ Warning: Could not install dependencies automatically.")
        print("  Please install manually using one of these commands:")
        print("    pip install -r requirements.txt")
        print("    pip install --user -r requirements.txt")
        print("    pip install --break-system-packages -r requirements.txt")
        print("  Or create a virtual environment:")
        print("    python -m venv venv")
        print("    source venv/bin/activate")
        print("    pip install -r requirements.txt")


def check_config():
    """Check if configuration files exist."""
    config_file = Path('configs/datasets.yaml')
    
    if not config_file.exists():
        print("\n⚠ Warning: configs/datasets.yaml not found!")
        print("  Please create this file before downloading datasets.")
        return False
    
    print(f"\n✓ Configuration file found: {config_file}")
    return True


def main():
    """Main setup function."""
    print("="*60)
    print("EEG-Epilepsy Project Setup")
    print("="*60)
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Check configuration
    has_config = check_config()
    
    # Print next steps
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    
    if has_config:
        print("1. Edit configs/datasets.yaml with your Google Drive file IDs")
        print("2. Run: python scripts/download_datasets.py")
    else:
        print("1. Create configs/datasets.yaml (you can use configs/datasets.yaml.example as a template)")
        print("2. Add your Google Drive file IDs to the configuration")
        print("3. Run: python scripts/download_datasets.py")
    
    print("\nFor more information, see the README.md file.")
    print("="*60)


if __name__ == '__main__':
    main()
