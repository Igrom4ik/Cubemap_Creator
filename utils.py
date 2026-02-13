import sys
import subprocess
import importlib

def is_pillow_installed():
    try:
        importlib.import_module('PIL')
        return True
    except ImportError:
        return False

def install_pillow():
    python_exe = sys.executable
    try:
        import PIL
        return True
    except ImportError:
        print("Pillow not found. Installing...")
        try:
            # Ensure pip is available
            subprocess.check_call([python_exe, "-m", "ensurepip"])
            # Upgrade pip
            subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
            # Install Pillow
            subprocess.check_call([python_exe, "-m", "pip", "install", "Pillow"])
            print("Pillow installed successfully!")
            return True
        except Exception as e:
            print(f"Failed to install Pillow: {e}")
            return False
