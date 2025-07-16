import os
import platform
import subprocess
import sys

def getVenv():
    if platform.system() == "Windows":
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")


def main():
    # activate virtualenv manually (only needed if dependencies must be loaded *in* this script)
    if os.path.isdir('venv'):
        python_exe = getVenv()
    else:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        python_exe = getVenv()
        subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], check=True)    

    # Run the actual processing script
    subprocess.run([python_exe, "ImageImports/converterscript.py"])

if __name__ == "__main__":
    main()

