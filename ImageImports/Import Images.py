import os
import platform
import subprocess
import sys

def main():
    # activate virtualenv manually (only needed if dependencies must be loaded *in* this script)
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate.bat")
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        activate_script = "source venv/bin/activate"
        python_exe = os.path.join("venv", "bin", "python")

    # Run the actual processing script
    subprocess.run([python_exe, "ImageImports/converterscript.py"])

if __name__ == "__main__":
    main()
