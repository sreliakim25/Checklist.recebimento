@echo off
cd /d "%~dp0"
echo ================================================
echo  Sistema de Checklists -- Obra 38
echo  Recanto das Oliveiras  UDE
echo ================================================

python -c "import flask" 2>nul || (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

python app.py
pause
