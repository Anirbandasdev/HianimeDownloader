#!/usr/bin/env python3
"""
Quick start script for HiAnime Downloader
Automatically sets up the environment and runs the enhanced version
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    system = platform.system().lower()
    
    if system == "windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    elif system == "darwin":  # macOS
        chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:  # Linux
        chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium-browser"]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Google Chrome detected")
            return True
    
    print("⚠️  Google Chrome not found. Please install Chrome for full functionality.")
    return False

def create_default_config():
    """Create default configuration if it doesn't exist"""
    config_file = Path("config.json")
    if not config_file.exists():
        print("🔧 Creating default configuration...")
        
        # Import and create config
        try:
            from tools.config_manager import ConfigManager
            config_manager = ConfigManager()
            print("✅ Default configuration created")
            return True
        except ImportError:
            print("⚠️  Could not create default config, will be created on first run")
            return True
    
    print("✅ Configuration file exists")
    return True

def setup_directories():
    """Set up necessary directories"""
    directories = ["downloads", "logs", "temp"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories set up")

def run_enhanced_app():
    """Run the enhanced application"""
    print("\n🚀 Starting Enhanced HiAnime Downloader...")
    print("=" * 60)
    
    try:
        # Try to import and run the enhanced app
        if os.path.exists("main_enhanced.py"):
            subprocess.run([sys.executable, "main_enhanced.py"] + sys.argv[1:])
        else:
            print("❌ Enhanced main file not found, falling back to original...")
            subprocess.run([sys.executable, "main.py"] + sys.argv[1:])
    except KeyboardInterrupt:
        print("\n👋 Thank you for using HiAnime Downloader!")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Main setup and run function"""
    print("🎌 HiAnime Downloader - Quick Start Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    # Check Chrome installation
    check_chrome()
    
    # Install dependencies if requirements.txt exists
    if os.path.exists("requirements.txt"):
        if not install_dependencies():
            print("⚠️  Continuing without installing dependencies...")
    
    # Set up configuration and directories
    create_default_config()
    setup_directories()
    
    # Run the application
    print("\n" + "=" * 60)
    run_enhanced_app()

if __name__ == "__main__":
    main()