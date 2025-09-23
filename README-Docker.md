# 🐳 Scaffold Forge - Docker Setup

Este guia mostra como executar o Scaffold Forge usando Docker e Docker Compose.

## 📋 Pré-requisitos

- Docker Desktop ou Docker Engine
- Docker Compose
- GitHub Personal Access Token

## 🚀 Execução Rápida

### 1. Clone e Configure

```bash
# Clone o repositório
git clone <seu-repositorio>
cd mini-gluon

# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env e adicione seu GitHub token
nano .env
```

### 2. Configure o GitHub Token

No arquivo `.env`, substitua:
```bash
GITHUB_TOKEN=seu_token_github_aqui
```

**Como obter o GitHub Token:**
1. Vá para GitHub → Settings → Developer settings → Personal access tokens
2. Clique em "Generate new token (classic)"
3. Selecione os scopes: `repo`, `workflow`, `write:packages`
4. Copie o token e cole no arquivo `.env`

### 3. Execute o Projeto

```bash
# Opção 1: Build rápido (recomendado)
./build-fast.sh

# Opção 2: Script automatizado
./build.sh

# Opção 3: Comando manual
docker-compose up --build

# Opção 4: Produção (com Nginx)
docker-compose --profile production up --build
```

**Nota**: O build rápido usa otimizações para reduzir o tempo de build de ~8 minutos para ~2 minutos.

## 🌐 Acessos

- **Frontend**: http://localhost:8000
- **API**: http://localhost:8000/api
- **MongoDB**: localhost:27017
- **Nginx** (produção): http://localhost:80

## 📊 Comandos Úteis

### Desenvolvimento
```bash
# Iniciar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose down && docker-compose up --build
```

### Manutenção
```bash
# Limpar volumes (CUIDADO: apaga dados do MongoDB)
docker-compose down -v

# Ver status dos containers
docker-compose ps

# Executar comandos no container
docker-compose exec scaffold-forge bash
docker-compose exec mongodb mongosh
```

### Logs e Debug
```bash
# Logs específicos
docker-compose logs scaffold-forge
docker-compose logs mongodb

# Logs em tempo real
docker-compose logs -f --tail=100
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Edite o arquivo `.env` para personalizar:

```bash
# MongoDB
MONGO_URL=mongodb://admin:password123@mongodb:27017/scaffold_forge?authSource=admin
DB_NAME=scaffold_forge

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Aplicação
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Portas Personalizadas

Edite o `docker-compose.yml`:

```yaml
ports:
  - "3000:8000"  # Mude 8000 para 3000
```

### SSL/HTTPS (Produção)

1. Coloque seus certificados em `./ssl/`
2. Descomente as linhas SSL no `nginx.conf`
3. Execute com profile production

## 🐛 Troubleshooting

### Problema: "GitHub token inválido"
```bash
# Verifique se o token está correto no .env
cat .env | grep GITHUB_TOKEN

# Teste o token
curl -H "Authorization: token SEU_TOKEN" https://api.github.com/user
```

### Problema: "MongoDB connection failed"
```bash
# Verifique se o MongoDB está rodando
docker-compose ps mongodb

# Ver logs do MongoDB
docker-compose logs mongodb
```

### Problema: "Port already in use"
```bash
# Verifique qual processo está usando a porta
netstat -tulpn | grep :8000

# Mude a porta no docker-compose.yml
```

### Problema: "Build failed"
```bash
# Limpe o cache do Docker
docker system prune -a

# Rebuild sem cache
docker-compose build --no-cache
```

## 📁 Estrutura dos Arquivos

```
mini-gluon/
├── Dockerfile              # Build da aplicação
├── docker-compose.yml      # Orquestração dos serviços
├── nginx.conf             # Configuração do Nginx
├── mongo-init.js          # Inicialização do MongoDB
├── .dockerignore          # Arquivos ignorados no build
├── env.example            # Exemplo de variáveis de ambiente
├── backend/               # Código Python/FastAPI
├── frontend/              # Código React
└── logs/                  # Logs da aplicação
```

## 🔒 Segurança

### Para Produção:
1. **Altere as senhas padrão** do MongoDB
2. **Use HTTPS** com certificados válidos
3. **Configure firewall** adequadamente
4. **Monitore logs** regularmente
5. **Mantenha imagens atualizadas**

### Secrets:
- Nunca commite o arquivo `.env`
- Use Docker secrets para produção
- Rotacione tokens regularmente

## 📈 Monitoramento

### Health Checks
```bash
# Verificar saúde dos serviços
curl http://localhost:8000/api/
curl http://localhost/health
```

### Métricas
- **MongoDB**: Acesse via mongosh
- **Aplicação**: Logs em `./logs/`
- **Nginx**: Logs de acesso e erro

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs`
2. Consulte este README
3. Abra uma issue no repositório
