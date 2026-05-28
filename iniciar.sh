#!/bin/bash
cd "$(dirname "$0")"
echo "================================================"
echo " Sistema de Checklists — Obra 38"
echo " Recanto das Oliveiras | UDE"
echo "================================================"

# Instalar dependências se necessário
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
fi

python3 app.py
