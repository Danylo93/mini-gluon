# 🚀 Instruções para Executar o Backend Refatorado

## 📋 Pré-requisitos

1. **Docker Desktop** instalado e rodando
2. **GitHub Token** configurado

## 🔧 Passos para Execução

### 1. **Iniciar o Docker Desktop**
- Abra o Docker Desktop
- Aguarde ele inicializar completamente (ícone verde na bandeja do sistema)

### 2. **Configurar Variáveis de Ambiente**
```bash
# Edite o arquivo .env com suas configurações
nano .env
```

**Configurações importantes:**
```env
# GitHub Configuration
GITHUB_TOKEN=seu_token_do_github_aqui

# Application Configuration
DEBUG=true
LOG_LEVEL=INFO
```

### 3. **Executar o Backend**

#### Opção A: Script Automatizado (Recomendado)
```bash
./start-backend.sh
```

#### Opção B: Comando Manual
```bash
# Parar containers existentes
docker-compose down

# Construir e iniciar
docker-compose up --build
```

## 🌐 Acessos Após Execução

- **API Principal**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/status/health
- **MongoDB**: localhost:27017

## 🔍 Verificar se Está Funcionando

### 1. **Health Check**
```bash
curl http://localhost:8000/api/status/health
```

### 2. **Listar Linguagens Suportadas**
```bash
curl http://localhost:8000/api/templates/languages
```

### 3. **Listar Templates Java**
```bash
curl http://localhost:8000/api/templates/java
```

## 🐛 Solução de Problemas

### Docker não está rodando
```bash
# Verificar se Docker está ativo
docker ps

# Se não estiver, iniciar Docker Desktop
```

### Erro de permissão
```bash
# No Windows, executar como administrador
# Ou usar WSL2
```

### Porta já em uso
```bash
# Parar containers
docker-compose down

# Verificar processos na porta 8000
netstat -ano | findstr :8000
```

### Problemas de build
```bash
# Limpar cache do Docker
docker system prune -a

# Reconstruir sem cache
docker-compose build --no-cache
```

## 📊 Logs e Monitoramento

### Ver logs em tempo real
```bash
docker-compose logs -f scaffold-forge
```

### Ver logs do MongoDB
```bash
docker-compose logs -f mongodb
```

### Status dos containers
```bash
docker-compose ps
```

## 🎯 Endpoints Principais

### Projetos
- `POST /api/projects/` - Criar novo projeto
- `GET /api/projects/` - Listar projetos
- `GET /api/projects/{id}` - Obter projeto por ID

### Templates
- `GET /api/templates/languages` - Linguagens suportadas
- `GET /api/templates/{language}` - Templates por linguagem
- `GET /api/templates/{language}/{template_id}/preview` - Preview do template

### Status
- `GET /api/status/health` - Health check
- `POST /api/status/check` - Criar status check

## 🔄 Comandos Úteis

### Parar tudo
```bash
docker-compose down
```

### Parar e remover volumes
```bash
docker-compose down -v
```

### Reconstruir apenas o backend
```bash
docker-compose up --build scaffold-forge
```

### Executar em background
```bash
docker-compose up -d
```

## 🎉 Sucesso!

Se tudo estiver funcionando, você verá:
- ✅ Containers rodando
- ✅ API respondendo em http://localhost:8000
- ✅ Health check retornando status "healthy"
- ✅ Documentação disponível em /docs

**O backend refatorado está rodando com a nova arquitetura modular! 🚀**
