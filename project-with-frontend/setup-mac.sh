#!/bin/bash

echo "========================================"
echo " Configurando ambiente do projeto EMG"
echo "========================================"

# Cria o ambiente virtual, caso não exista
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "Ambiente virtual já existe."
fi

# Ativa o ambiente
source venv/bin/activate

# Atualiza o pip
python -m pip install --upgrade pip

# Instala as dependências
pip install -r ../requirements.txt

echo ""
echo "========================================"
echo " Ambiente configurado com sucesso!"
echo "========================================"
echo ""

echo "Executando aplicação..."
python src/gui.py
