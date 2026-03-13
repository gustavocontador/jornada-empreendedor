# API Endpoints - Jornada do Empreendedor de Sucesso

## Base URL
```
http://localhost:8000/api/v1
```

## Autenticação

Todos os endpoints (exceto `/health` e `/`) requerem autenticação via JWT Bearer token.

### Header de Autenticação
```
Authorization: Bearer <access_token>
```

---

## 1. Autenticação (`/api/v1/auth`)

### POST /auth/register
Cria nova conta de usuário.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "senha123",
  "full_name": "João Silva"
}
```

**Response (201):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "João Silva",
    "is_active": true,
    "is_admin": false,
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

---

### POST /auth/login
Faz login e retorna tokens JWT.

**Body (Form Data):**
```
username: user@example.com
password: senha123
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

---

### POST /auth/refresh
Renova access token usando refresh token.

**Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access_token": "novo_token...",
  "refresh_token": "novo_refresh_token...",
  "token_type": "bearer",
  "user": { ... }
}
```

---

### GET /auth/me
Retorna dados do usuário logado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "João Silva",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## 2. Assessments (`/api/v1/assessments`)

### POST /assessments/
Inicia novo assessment.

**Body:**
```json
{
  "metadata": {
    "device": "mobile",
    "timezone": "America/Sao_Paulo"
  }
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "status": "in_progress",
  "started_at": "2025-01-15T10:30:00Z",
  "completed_at": null,
  "current_question_index": 0,
  "total_questions": 105,
  "progress_percentage": 0.0,
  "metadata": { ... },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

### GET /assessments/
Lista todos os assessments do usuário logado.

**Query Params:**
- `skip` (int, default: 0): Paginação
- `limit` (int, default: 20): Número de resultados
- `status_filter` (string, optional): `in_progress`, `completed`, `abandoned`

**Response (200):**
```json
[
  {
    "id": "uuid",
    "status": "completed",
    "started_at": "2025-01-15T10:30:00Z",
    "completed_at": "2025-01-15T11:00:00Z",
    "progress_percentage": 100.0,
    ...
  }
]
```

---

### GET /assessments/{assessment_id}
Retorna assessment específico.

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "status": "in_progress",
  "current_question_index": 42,
  "total_questions": 105,
  "progress_percentage": 40.0,
  ...
}
```

---

### POST /assessments/{assessment_id}/complete
Finaliza assessment e calcula resultados.

**Response (200):**
```json
{
  "message": "Assessment finalizado com sucesso",
  "assessment_id": "uuid",
  "status": "completed",
  "scores_calculated": true
}
```

---

## 3. Questions (`/api/v1/questions`)

### GET /questions/
Lista perguntas do questionário.

**Query Params:**
- `skip` (int, default: 0): Paginação
- `limit` (int, default: 20): Número de resultados
- `section` (string, optional): Filtrar por seção

**Response (200):**
```json
{
  "total": 105,
  "skip": 0,
  "limit": 20,
  "section": null,
  "questions": [
    {
      "id": "q001",
      "secao": "intro",
      "ordem": 1,
      "texto": "Qual é o seu nome completo?",
      "tipo": "text",
      "obrigatorio": true
    },
    ...
  ],
  "metadata": {
    "nome": "Jornada do Empreendedor de Sucesso",
    "versao": "1.0.0",
    "total_perguntas": 105
  }
}
```

---

### GET /questions/sections
Lista todas as seções do questionário.

**Response (200):**
```json
[
  {
    "id": "intro",
    "nome": "Informações Iniciais",
    "descricao": "Contexto sobre você e seu negócio",
    "ordem": 1,
    "tempo_estimado": "3 min",
    "total_perguntas": 5
  },
  ...
]
```

---

### GET /questions/{question_id}
Retorna pergunta específica.

**Response (200):**
```json
{
  "id": "q042",
  "secao": "gestao_lideranca",
  "ordem": 2,
  "texto": "Fico frustrado quando reuniões ou planejamentos atrasam a execução.",
  "tipo": "likert_5",
  "escala": {
    "1": "Discordo totalmente",
    "5": "Concordo totalmente"
  },
  "pontuacao": { ... }
}
```

---

## 4. Responses (`/api/v1/responses`)

### POST /responses/
Salva resposta de uma pergunta.

**Body:**
```json
{
  "assessment_id": "uuid",
  "question_id": "uuid",
  "answer_value": 4
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "assessment_id": "uuid",
  "question_id": "uuid",
  "answer_value": 4,
  "answered_at": "2025-01-15T10:35:00Z"
}
```

---

### GET /responses/{assessment_id}
Lista todas as respostas de um assessment.

**Response (200):**
```json
[
  {
    "id": "uuid",
    "assessment_id": "uuid",
    "question_id": "uuid",
    "answer_value": 4,
    "answered_at": "2025-01-15T10:35:00Z"
  },
  ...
]
```

---

### PATCH /responses/{response_id}
Atualiza resposta existente.

**Body:**
```json
{
  "answer_value": 5
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "answer_value": 5,
  "answered_at": "2025-01-15T10:35:00Z"
}
```

---

## 5. Results (`/api/v1/results`)

### GET /results/{assessment_id}
Retorna resultados completos de um assessment.

**Response (200):**
```json
{
  "id": "uuid",
  "assessment_id": "uuid",
  "user_id": "uuid",
  "scores": {
    "disc": {
      "d": 75.5,
      "i": 45.2,
      "s": 30.1,
      "c": 60.8,
      "profile": "DC",
      "primary": "D",
      "description": "Dominante e Consciencioso..."
    },
    "spiral": {
      "red": 65.3,
      "blue": 45.2,
      "orange": 80.5,
      "primary": "orange",
      "secondary": "red",
      "description": "Moderno/Conquista..."
    },
    "paei": {
      "p": 85.2,
      "a": 40.1,
      "e": 70.5,
      "i": 35.0,
      "code": "PaeI",
      "style": "Produtor-Empreendedor"
    },
    "enneagram": {
      "type": 8,
      "wing": "8w7",
      "description": "O Desafiador..."
    },
    "valores": {
      "primary": "resultado",
      "secondary": "inovacao",
      "tertiary": "autonomia"
    },
    "arquetipos": {
      "primary": "executor",
      "secondary": "criativo",
      "tertiary": "lider"
    },
    "interpretations": {
      "key_strengths": [...],
      "key_challenges": [...],
      "leadership_style": "..."
    },
    "recommendations": {
      "gestao_pessoas": [...],
      "gestao_financeira": [...],
      "processos_organizacao": [...]
    }
  },
  "calculated_at": "2025-01-15T11:00:00Z"
}
```

---

### GET /results/{assessment_id}/summary
Retorna resumo simplificado dos resultados.

**Response (200):**
```json
{
  "assessment_id": "uuid",
  "calculated_at": "2025-01-15T11:00:00Z",
  "disc": {
    "profile": "DC",
    "primary": "D",
    "description": "..."
  },
  "spiral": {
    "primary": "orange",
    "secondary": "red"
  },
  "paei": {
    "code": "PaeI",
    "style": "Produtor-Empreendedor"
  },
  "key_strengths": ["...", "...", "..."],
  "key_challenges": ["...", "...", "..."],
  "top_recommendations": [...]
}
```

---

## 6. Reports (`/api/v1/reports`)

### POST /reports/generate
Gera relatório PDF.

**Body:**
```json
{
  "assessment_id": "uuid",
  "report_type": "simplified",
  "metadata": {
    "language": "pt-BR"
  }
}
```

**Tipos disponíveis:**
- `simplified`: Relatório resumido (5-10 páginas)
- `complete`: Relatório completo (30-40 páginas)

**Response (201):**
```json
{
  "id": "uuid",
  "assessment_id": "uuid",
  "user_id": "uuid",
  "report_type": "simplified",
  "status": "pending",
  "file_path": null,
  "created_at": "2025-01-15T11:05:00Z",
  "metadata": { ... }
}
```

---

### GET /reports/{report_id}
Retorna metadados do relatório.

**Response (200):**
```json
{
  "id": "uuid",
  "assessment_id": "uuid",
  "report_type": "simplified",
  "status": "completed",
  "file_path": "/path/to/report.pdf",
  "download_url": "/api/v1/reports/{uuid}/download",
  "created_at": "2025-01-15T11:05:00Z"
}
```

---

### GET /reports/{report_id}/download
Faz download do PDF do relatório.

**Response (200):**
- Content-Type: `application/pdf`
- Filename: `relatorio_simplified_{uuid}.pdf`

---

## 7. Admin (`/api/v1/admin`)

**Requer:** `is_admin = True`

### GET /admin/users
Lista todos os usuários (admin only).

**Query Params:**
- `skip` (int, default: 0)
- `limit` (int, default: 50)

**Response (200):**
```json
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "João Silva",
    "is_active": true,
    "is_admin": false,
    "created_at": "2025-01-15T10:30:00Z"
  },
  ...
]
```

---

### GET /admin/assessments
Lista todos os assessments do sistema (admin only).

**Query Params:**
- `skip`, `limit`, `status_filter`

**Response (200):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "status": "completed",
    ...
  }
]
```

---

### GET /admin/dashboard
Retorna dashboard com estatísticas do sistema.

**Response (200):**
```json
{
  "users": {
    "total": 150,
    "active": 142,
    "inactive": 8
  },
  "assessments": {
    "total": 320,
    "completed": 245,
    "in_progress": 75,
    "completion_rate": 76.56
  },
  "results": {
    "total": 245
  },
  "reports": {
    "total": 180,
    "completed": 165
  },
  "top_users": [
    {
      "user_id": "uuid",
      "email": "user@example.com",
      "full_name": "João Silva",
      "assessment_count": 15
    }
  ]
}
```

---

### POST /admin/users/{user_id}/toggle-active
Ativa/desativa um usuário (admin only).

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": false,
  ...
}
```

---

## 8. Health & Root

### GET /health
Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "Jornada do Empreendedor de Sucesso",
  "version": "1.0.0"
}
```

---

### GET /
Informações da API.

**Response (200):**
```json
{
  "message": "Jornada do Empreendedor de Sucesso API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Erro na requisição |
| 401 | Unauthorized - Token inválido ou ausente |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Erro de validação |
| 500 | Internal Server Error - Erro do servidor |

---

## Fluxo Típico de Uso

1. **Registro/Login:**
   - POST `/auth/register` ou POST `/auth/login`
   - Salvar `access_token` e `refresh_token`

2. **Iniciar Assessment:**
   - POST `/assessments/`
   - Guardar `assessment_id`

3. **Carregar Perguntas:**
   - GET `/questions/` (com paginação ou filtro por seção)

4. **Responder Perguntas:**
   - POST `/responses/` para cada pergunta
   - PATCH `/responses/{id}` se precisar alterar

5. **Finalizar Assessment:**
   - POST `/assessments/{id}/complete`

6. **Ver Resultados:**
   - GET `/results/{assessment_id}` (completo)
   - GET `/results/{assessment_id}/summary` (resumido)

7. **Gerar Relatório:**
   - POST `/reports/generate`
   - GET `/reports/{id}` (verificar status)
   - GET `/reports/{id}/download` (quando status = completed)

---

## Documentação Interativa

Acesse a documentação interativa da API (Swagger):
```
http://localhost:8000/docs
```

Ou use ReDoc:
```
http://localhost:8000/redoc
```
