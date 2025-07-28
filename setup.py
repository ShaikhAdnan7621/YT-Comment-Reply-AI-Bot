#!/usr/bin/env python3
"""
Setup script for YouTube Comment AI Bot
Supports multiple installation methods
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required. Current version:", sys.version)
        sys.exit(1)
    print("✅ Python version:", sys.version.split()[0])

def install_with_pip():
    """Install using pip and virtual environment"""
    print("\n🔧 Installing with pip + virtual environment...")
    
    # Create virtual environment
    if platform.system() == "Windows":
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Install dependencies
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    print("✅ Installation completed!")
    print(f"\nTo run:")
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print("  python main.py")

def install_with_conda():
    """Install using conda environment"""
    print("\n🔧 Installing with conda...")
    subprocess.run(["conda", "env", "create", "-f", "environment.yml"])
    print("✅ Installation completed!")
    print("\nTo run:")
    print("  conda activate commentbot")
    print("  python main.py")

def main():
    print("🚀 YouTube Comment AI Bot Setup")
    print("=" * 40)
    
    check_python_version()
    
    print("\nChoose installation method:")
    print("1. Pip + Virtual Environment (Recommended)")
    print("2. Conda Environment")
    print("3. Global pip install (Not recommended)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        install_with_pip()
    elif choice == "2":
        try:
            install_with_conda()
        except FileNotFoundError:
            print("❌ Conda not found. Please install Anaconda/Miniconda first.")
            print("Or choose option 1 for pip installation.")
    elif choice == "3":
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Global installation completed!")
        print("Run: python main.py")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()