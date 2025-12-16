import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime

def clean_build_dirs():
    """Removes 'dist' and 'build' directories if they exist."""
    print("Cleanings 'dist' and 'build' directories...")
    for d in ["dist", "build"]:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"Removed {d}")
            except Exception as e:
                print(f"Error removing {d}: {e}")
                sys.exit(1)

def run_pyinstaller():
    """Runs PyInstaller using the current Python interpreter."""
    print("Running PyInstaller...")
    try:
        # Using sys.executable ensures we use the same python environment
        cmd = [sys.executable, "-m", "PyInstaller", "TFTAutoAccept.spec"]
        subprocess.check_call(cmd)
        print("PyInstaller finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def create_zip_release():
    """Zips the built executable into the releases directory."""
    releases_dir = "releases"
    if not os.path.exists(releases_dir):
        os.makedirs(releases_dir)
        print(f"Created '{releases_dir}' directory.")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    zip_name = f"TFTAutoAccept-{timestamp}.zip"
    zip_path = os.path.join(releases_dir, zip_name)
    
    exe_name = "TFTAutoAccept.exe" if sys.platform == "win32" else "TFTAutoAccept"
    source_file = os.path.join("dist", exe_name)
    
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' does not exist.")
        sys.exit(1)

    print(f"Zipping release to {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_file, arcname=exe_name)
        print(f"Done! Release created at {zip_path}")
    except Exception as e:
        print(f"Error creating zip file: {e}")
        sys.exit(1)

def main():
    print("🔨 Building TFT Auto Accept...")
    clean_build_dirs()
    run_pyinstaller()
    create_zip_release()

if __name__ == "__main__":
    main()
