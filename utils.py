import sys
import subprocess
import importlib

def is_pillow_installed():
    try:
        importlib.import_module('PIL')
        return True
    except ImportError:
        return False

def install_pillow(force_reinstall=False):
    python_exe = sys.executable
    try:
        if not force_reinstall:
            import PIL
            return True
    except ImportError:
        pass

    try:
        # Ensure pip is available
        subprocess.check_call([python_exe, "-m", "ensurepip"])
        # Upgrade pip
        subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
        # Install or force-reinstall Pillow
        if force_reinstall:
            subprocess.check_call([
                python_exe,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--force-reinstall",
                "Pillow",
            ])
        else:
            subprocess.check_call([python_exe, "-m", "pip", "install", "Pillow"])
        print("Pillow installed successfully!")
        return True
    except Exception as e:
        print(f"Failed to install Pillow: {e}")
        return False
