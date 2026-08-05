@echo off

python -m venv venv 2>nul || py -m venv venv

call venv\Scripts\activate

if exist requirements.txt (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo Ambiente pronto!
cmd /k