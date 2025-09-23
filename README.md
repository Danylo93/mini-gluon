# 🚀 Scaffold Forge

Sistema de geração de templates de projetos com interface moderna e backend refatorado.

## 🛠️ Como Executar

### 1. Pré-requisitos
- Docker Desktop instalado e rodando
- GitHub Token (opcional, para criar repositórios)

### 2. Executar o Projeto
```bash
# Script automatizado
./start.sh

# OU manualmente
docker-compose up --build
```

### 3. Acessar
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs

## 🏗️ Arquitetura

### Backend Refatorado
- ✅ Arquitetura modular (models, services, repositories, routers)
- ✅ Validação robusta com Pydantic
- ✅ Tratamento de erros centralizado
- ✅ Logging estruturado
- ✅ Testes unitários

### Frontend
- ✅ Interface React moderna
- ✅ Componentes reutilizáveis
- ✅ Design responsivo

### Infraestrutura
- ✅ Docker multi-stage build
- ✅ MongoDB para persistência
- ✅ Nginx como proxy reverso

## 🔧 Comandos Úteis

```bash
# Parar containers
docker-compose down

# Ver logs
docker-compose logs -f

# Reconstruir
docker-compose up --build

# Executar em background
docker-compose up -d
```

## 📊 Funcionalidades

- ✅ Criação de projetos com templates
- ✅ Integração com GitHub
- ✅ Múltiplas linguagens (Java, .NET)
- ✅ Interface intuitiva
- ✅ API REST documentada

## 🎯 Tecnologias

- **Frontend**: React, Tailwind CSS
- **Backend**: FastAPI, Python 3.11
- **Banco**: MongoDB
- **Container**: Docker, Docker Compose
- **Proxy**: Nginx