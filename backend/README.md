# Scaffold Forge Backend

Backend API para o sistema de geração de templates de projetos Scaffold Forge.

## 🏗️ Arquitetura

O backend foi refatorado seguindo padrões modernos de desenvolvimento e escalabilidade:

### Estrutura de Diretórios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── config/                 # Configurações
│   │   ├── __init__.py
│   │   └── settings.py         # Configurações centralizadas
│   ├── core/                   # Componentes centrais
│   │   ├── __init__.py
│   │   ├── database.py         # Conexão com banco de dados
│   │   ├── exceptions.py       # Exceções customizadas
│   │   └── logging.py          # Configuração de logging
│   ├── models/                 # Modelos de dados
│   │   ├── __init__.py
│   │   ├── base.py            # Modelos base
│   │   ├── project.py         # Modelos de projeto
│   │   ├── template.py        # Modelos de template
│   │   └── status.py          # Modelos de status
│   ├── repositories/          # Camada de acesso a dados
│   │   ├── __init__.py
│   │   ├── base.py           # Repository base
│   │   ├── project.py        # Repository de projetos
│   │   └── status.py         # Repository de status
│   ├── services/             # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── github_service.py # Serviço do GitHub
│   │   ├── template_service.py # Serviço de templates
│   │   └── project_service.py # Serviço de projetos
│   ├── routers/              # Endpoints da API
│   │   ├── __init__.py
│   │   ├── projects.py       # Endpoints de projetos
│   │   ├── templates.py      # Endpoints de templates
│   │   └── status.py         # Endpoints de status
│   └── utils/                # Utilitários
│       ├── __init__.py
│       └── validators.py     # Funções de validação
├── tests/                    # Testes
│   ├── __init__.py
│   ├── conftest.py          # Configuração do pytest
│   └── unit/                # Testes unitários
│       └── test_utils.py
├── requirements.txt          # Dependências
├── env.example              # Exemplo de variáveis de ambiente
├── run.py                   # Script de execução
└── README.md               # Este arquivo
```

## 🚀 Principais Melhorias

### 1. **Arquitetura Modular**
- Separação clara de responsabilidades
- Padrão Repository para acesso a dados
- Serviços para lógica de negócio
- Routers para endpoints da API

### 2. **Configuração Centralizada**
- Configurações via variáveis de ambiente
- Validação automática de configurações
- Suporte a diferentes ambientes (dev, prod)

### 3. **Tratamento de Erros Robusto**
- Exceções customizadas
- Tratamento centralizado de erros
- Logs estruturados

### 4. **Validação e Segurança**
- Validação de dados com Pydantic
- Sanitização de inputs
- Middleware de segurança

### 5. **Logging Estruturado**
- Logs centralizados e configuráveis
- Diferentes níveis de log
- Rastreamento de requisições

### 6. **Testes**
- Testes unitários
- Fixtures para testes
- Cobertura de código

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados e serialização
- **Motor**: Driver assíncrono para MongoDB
- **PyGithub**: Integração com GitHub API
- **Pytest**: Framework de testes
- **Uvicorn**: Servidor ASGI

## 📋 Pré-requisitos

- Python 3.8+
- MongoDB
- Token do GitHub

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd mini-gluon/backend
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute o servidor**
```bash
python run.py
```

## 🌐 Endpoints da API

### Projetos
- `POST /api/projects/` - Criar novo projeto
- `GET /api/projects/` - Listar projetos
- `GET /api/projects/{id}` - Obter projeto por ID
- `PATCH /api/projects/{id}/status` - Atualizar status do projeto
- `DELETE /api/projects/{id}` - Deletar projeto

### Templates
- `GET /api/templates/languages` - Listar linguagens suportadas
- `GET /api/templates/{language}` - Listar templates por linguagem
- `GET /api/templates/{language}/{template_id}` - Obter detalhes do template
- `GET /api/templates/{language}/{template_id}/preview` - Preview do template

### Status
- `GET /api/status/health` - Health check
- `POST /api/status/check` - Criar status check
- `GET /api/status/checks` - Listar status checks

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app

# Executar testes específicos
pytest tests/unit/test_utils.py
```

## 📊 Monitoramento

- **Health Check**: `/api/status/health`
- **Logs**: Configuráveis via variáveis de ambiente
- **Métricas**: Tempo de processamento nas headers de resposta

## 🔒 Segurança

- Validação de entrada em todas as APIs
- Sanitização de dados
- CORS configurável
- Rate limiting (configurável)
- Headers de segurança

## 🚀 Deploy

O backend está preparado para deploy em:
- Docker containers
- Cloud providers (AWS, GCP, Azure)
- Servidores tradicionais

## 📝 Desenvolvimento

### Adicionando Novos Endpoints

1. Crie o modelo em `app/models/`
2. Implemente o repository em `app/repositories/`
3. Crie o serviço em `app/services/`
4. Adicione o router em `app/routers/`
5. Registre o router em `app/main.py`

### Adicionando Novos Templates

1. Adicione o template em `app/services/template_service.py`
2. Defina os arquivos e variáveis necessárias
3. Teste com o endpoint de preview

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
