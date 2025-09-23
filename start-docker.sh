#!/bin/bash

# Script para iniciar Docker Desktop no Windows
echo "🐳 Verificando status do Docker..."

# Verifica se o Docker está rodando
if docker info >/dev/null 2>&1; then
    echo "✅ Docker está rodando!"
    exit 0
fi

echo "❌ Docker não está rodando. Tentando iniciar..."

# No Windows, tenta iniciar o Docker Desktop
if command -v "C:\Program Files\Docker\Docker\"Docker Desktop.exe" >/dev/null 2>&1; then
    echo "🚀 Iniciando Docker Desktop..."
    "C:\Program Files\Docker\Docker\"Docker Desktop.exe" &
    
    echo "⏳ Aguardando Docker inicializar..."
    for i in {1..30}; do
        if docker info >/dev/null 2>&1; then
            echo "✅ Docker iniciado com sucesso!"
            exit 0
        fi
        echo "Aguardando... ($i/30)"
        sleep 2
    done
    
    echo "❌ Timeout: Docker não iniciou em 60 segundos"
    echo "💡 Tente iniciar o Docker Desktop manualmente e execute novamente"
    exit 1
else
    echo "❌ Docker Desktop não encontrado em C:\Program Files\Docker\Docker\""
    echo "💡 Instale o Docker Desktop ou inicie manualmente"
    exit 1
fi
