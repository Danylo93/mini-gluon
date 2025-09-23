#!/bin/bash

# Script simples para iniciar o Scaffold Forge

echo "🚀 Iniciando Scaffold Forge..."

# Verificar se o Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker Desktop primeiro."
    exit 1
fi

echo "✅ Docker está rodando!"

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Criando arquivo .env..."
    cat > .env << EOF
GITHUB_TOKEN=your_github_token_here
DEBUG=true
LOG_LEVEL=INFO
EOF
    echo "📝 Configure seu GITHUB_TOKEN no arquivo .env"
    read -p "Pressione Enter após configurar..."
fi

echo "🔨 Iniciando containers..."
docker-compose up --build

echo "🎉 Projeto iniciado!"
echo "🌐 Frontend: http://localhost:80"
echo "🔧 Backend: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
