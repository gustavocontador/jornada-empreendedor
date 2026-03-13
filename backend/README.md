# Backend - Jornada do Empreendedor de Sucesso

API REST completa em FastAPI para sistema de assessment comportamental de empreendedores.

## 🚀 Tecnologias

- **FastAPI** 0.109.0 - Framework web moderno
- **PostgreSQL** 15+ - Banco de dados relacional
- **SQLAlchemy** 2.0 - ORM
- **Pydantic** 2.5 - Validação de dados
- **JWT** - Autenticação
- **WeasyPrint** - Geração de PDFs
- **Plotly** - Gráficos

## 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL 15+
- pip ou poetry

## 🔧 Instalação

### 1. Clone o repositório e entre na pasta backend

```bash
cd backend
```

### 2. Crie ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 5. Crie o banco de dados

```bash
createdb jornada_empreendedor
```

### 6. Execute migrations

```bash
alembic upgrade head
```

### 7. Inicie o servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Login Admin Padrão

Criado automaticamente no primeiro startup:

- **Email**: admin@example.com
- **Senha**: admin123

⚠️ **IMPORTANTE**: Altere a senha em produção!

## 🗂️ Estrutura de Pastas

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── assessments.py
│   │       │   ├── questions.py
│   │       │   ├── responses.py
│   │       │   ├── results.py
│   │       │   ├── reports.py
│   │       │   └── admin.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   ├── assessment.py
│   │   ├── question.py
│   │   ├── response.py
│   │   ├── result.py
│   │   └── report.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── assessment.py
│   │   ├── response.py
│   │   ├── result.py
│   │   └── report.py
│   ├── services/
│   │   ├── calculators/
│   │   │   ├── scoring_engine.py
│   │   │   ├── disc_calculator.py
│   │   │   ├── spiral_calculator.py
│   │   │   ├── paei_calculator.py
│   │   │   ├── enneagram_calculator.py
│   │   │   ├── valores_calculator.py
│   │   │   ├── arquetipos_calculator.py
│   │   │   └── interpretations_generator.py
│   │   ├── questions_loader.py
│   │   └── reports/
│   ├── utils/
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 🎯 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/register` - Criar conta
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Dados do usuário

### Assessments
- `POST /api/v1/assessments/` - Iniciar assessment
- `GET /api/v1/assessments/` - Listar assessments
- `POST /api/v1/assessments/{id}/complete` - Finalizar e calcular

### Questions
- `GET /api/v1/questions/` - Listar perguntas
- `GET /api/v1/questions/sections` - Listar seções

### Responses
- `POST /api/v1/responses/` - Salvar resposta
- `GET /api/v1/responses/{assessment_id}` - Listar respostas

### Results
- `GET /api/v1/results/{assessment_id}` - Resultados completos
- `GET /api/v1/results/{assessment_id}/summary` - Resumo

### Reports
- `POST /api/v1/reports/generate` - Gerar PDF
- `GET /api/v1/reports/{id}/download` - Download PDF

### Admin
- `GET /api/v1/admin/users` - Listar usuários
- `GET /api/v1/admin/dashboard` - Dashboard

## 🧪 Testes

```bash
pytest
```

## 🐳 Docker

### Build

```bash
docker build -t jornada-backend .
```

### Run

```bash
docker run -p 8000:8000 --env-file .env jornada-backend
```

## 📊 Frameworks de Assessment

O sistema calcula 6 frameworks psicométricos:

1. **DISC** - Comportamento (4 dimensões)
2. **Espiral Dinâmica** - Consciência evolutiva (8 níveis)
3. **PAEI (Adizes)** - Estilo de gestão (4 papéis)
4. **Eneagrama** - Motivações profundas (9 tipos)
5. **Valores Empresariais** - 10 valores priorizados
6. **Arquétipos** - Perfil de contratação (9 tipos)

## 🔄 Fluxo Completo

```
1. Usuário se cadastra (POST /auth/register)
2. Faz login (POST /auth/login) → recebe JWT
3. Inicia assessment (POST /assessments/)
4. Responde perguntas (POST /responses/ para cada pergunta)
5. Finaliza assessment (POST /assessments/{id}/complete)
   → Sistema calcula todos os scores automaticamente
6. Visualiza resultados (GET /results/{assessment_id})
7. Gera relatório PDF (POST /reports/generate)
8. Baixa relatório (GET /reports/{id}/download)
```

## 📈 Performance

- **Cálculo de scores**: ~80-100ms
- **Geração de PDF**: ~2-5s
- **API response time**: <100ms (endpoints simples)

## 🔒 Segurança

- Senhas com bcrypt (12 rounds)
- JWT com expiração (15min access, 7 dias refresh)
- CORS configurado
- Validação de ownership
- Admin-only endpoints protegidos

## 🐛 Troubleshooting

### Erro de conexão com banco
```bash
# Verifique se PostgreSQL está rodando
pg_isready

# Teste conexão
psql -U user -d jornada_empreendedor
```

### Erro ao carregar perguntas
```bash
# Verifique se o arquivo YAML existe
ls ../questions/questionario-completo-v1.yaml
```

## 📝 Licença

Proprietary - Todos os direitos reservados

## 👥 Contribuição

Sistema desenvolvido para uso interno.

---

**Versão**: 1.0.0
**Data**: 2026-03-13
