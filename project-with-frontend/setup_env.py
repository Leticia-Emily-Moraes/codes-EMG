import platform
import subprocess
import sys
from pathlib import Path

venv = Path("venv")

if not venv.exists():
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

if platform.system() == "Windows":
    python = Path("venv/Scripts/python.exe")
else:
    python = Path("venv/bin/python")

subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
subprocess.run([str(python), "-m", "pip", "install", "-r", "../requirements.txt"])

print("Ambiente configurado com sucesso!")
