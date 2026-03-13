# Guia de Integração Frontend-Backend

## Configuração Inicial

### 1. Variáveis de Ambiente

Criar arquivo `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Para produção, ajustar para URL real da API.

### 2. Iniciar Servidores

**Backend (FastAPI):**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Frontend (Next.js):**
```bash
cd frontend
npm run dev
```

Frontend estará em: http://localhost:3000
Backend estará em: http://localhost:8000

## Endpoints da API

### Autenticação

#### POST /api/auth/register
**Request:**
```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "token": "eyJ...",
  "user": {
    "id": "uuid",
    "name": "João Silva",
    "email": "joao@email.com",
    "role": "user",
    "createdAt": "2026-03-13T10:00:00Z",
    "updatedAt": "2026-03-13T10:00:00Z"
  }
}
```

#### POST /api/auth/login
**Request:**
```json
{
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "token": "eyJ...",
  "user": { ... }
}
```

### Assessments

#### POST /api/assessments
Cria novo assessment.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "id": "uuid",
  "userId": "uuid",
  "status": "in_progress",
  "currentQuestionIndex": 0,
  "totalQuestions": 50,
  "startedAt": "2026-03-13T10:00:00Z",
  "createdAt": "2026-03-13T10:00:00Z",
  "updatedAt": "2026-03-13T10:00:00Z"
}
```

#### GET /api/assessments/:id
Busca assessment por ID.

**Headers:** `Authorization: Bearer {token}`

#### GET /api/questions
Lista todas as perguntas.

**Response:**
```json
[
  {
    "id": "uuid",
    "text": "Eu prefiro trabalhar sozinho do que em equipe",
    "type": "likert_5",
    "options": null,
    "category": "comportamento",
    "order": 1,
    "frameworks": ["disc", "spiral_dynamics"]
  }
]
```

#### POST /api/responses
Salva resposta de uma pergunta.

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "assessmentId": "uuid",
  "questionId": "uuid",
  "response": 4
}
```

#### GET /api/assessments/:id/responses
Lista todas as respostas de um assessment.

**Headers:** `Authorization: Bearer {token}`

#### POST /api/assessments/:id/complete
Finaliza assessment e gera resultados.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "message": "Assessment completed successfully",
  "resultId": "uuid"
}
```

### Resultados

#### GET /api/results/:id
Busca resultado completo.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "id": "uuid",
  "assessmentId": "uuid",
  "userId": "uuid",
  "disc": {
    "D": 75,
    "I": 60,
    "S": 45,
    "C": 55,
    "profile": "Di",
    "description": "Perfil dominante e influente..."
  },
  "spiral_dynamics": {
    "beige": 10,
    "purple": 15,
    "red": 25,
    "blue": 30,
    "orange": 65,
    "green": 45,
    "yellow": 35,
    "turquoise": 20,
    "dominant_color": "orange",
    "description": "Foco em conquistas e sucesso..."
  },
  "paei": {
    "P": 70,
    "A": 55,
    "E": 80,
    "I": 40,
    "code": "PaEi",
    "description": "Perfil empreendedor com foco em produção..."
  },
  "enneagram": {
    "type": 3,
    "wing": "3w4",
    "description": "O Realizador com asa 4...",
    "strengths": ["Ambicioso", "Adaptável", "Eficiente"],
    "challenges": ["Workaholism", "Dificuldade em relaxar"]
  },
  "values": {
    "top_values": ["Sucesso", "Autonomia", "Inovação"],
    "descriptions": {
      "Sucesso": "Você valoriza conquistas e resultados...",
      "Autonomia": "Liberdade para tomar decisões...",
      "Inovação": "Criar coisas novas..."
    }
  },
  "overall_summary": "Você é um empreendedor nato...",
  "recommendations": [
    "Desenvolva habilidades de delegação",
    "Invista em networking",
    "Balance trabalho e vida pessoal"
  ],
  "createdAt": "2026-03-13T10:30:00Z",
  "updatedAt": "2026-03-13T10:30:00Z"
}
```

#### GET /api/results/:id/pdf
Baixa relatório em PDF.

**Headers:** `Authorization: Bearer {token}`

**Response:** Binary PDF file

### Admin (requer role=admin)

#### GET /api/admin/stats
Estatísticas gerais.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "totalUsers": 150,
  "totalAssessments": 200,
  "completedAssessments": 180,
  "inProgressAssessments": 20
}
```

#### GET /api/admin/assessments/recent
Assessments recentes.

**Response:**
```json
[
  {
    "id": "uuid",
    "userId": "uuid",
    "userName": "João Silva",
    "status": "completed",
    "createdAt": "2026-03-13T10:00:00Z",
    "completedAt": "2026-03-13T10:30:00Z"
  }
]
```

#### GET /api/admin/clients
Lista todos os clientes.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "João Silva",
    "email": "joao@email.com",
    "createdAt": "2026-03-10T10:00:00Z",
    "assessmentsCount": 2,
    "completedAssessmentsCount": 2,
    "latestAssessmentId": "uuid",
    "latestResultId": "uuid"
  }
]
```

## Fluxo de Usuário

### 1. Cadastro/Login
1. Usuário acessa landing page (`/`)
2. Clica em "Começar Agora" ou "Cadastrar"
3. Preenche formulário de cadastro (`/register`)
4. Backend valida e retorna token + dados do usuário
5. Frontend salva token no localStorage
6. Redireciona para `/questionario`

### 2. Questionário
1. Frontend chama `POST /api/assessments` para criar novo
2. Carrega perguntas com `GET /api/questions`
3. Para cada resposta:
   - Usuário responde
   - Frontend chama `POST /api/responses` (auto-save com debounce)
   - Atualiza estado local
4. Ao finalizar, chama `POST /api/assessments/:id/complete`
5. Backend processa resultados
6. Redireciona para `/resultado/:resultId`

### 3. Visualização de Resultados
1. Frontend carrega resultado com `GET /api/results/:id`
2. Renderiza tabs com gráficos de cada framework
3. Exibe recomendações
4. Botão para download PDF chama `GET /api/results/:id/pdf`

## Tratamento de Erros

### Erro 401 (Não Autorizado)
- Interceptor Axios detecta
- Remove token do localStorage
- Redireciona para `/login`

### Erro 403 (Sem Permissão)
- Usuário tentou acessar área admin sem ser admin
- Redireciona para página inicial

### Erro 404 (Não Encontrado)
- Recurso não existe
- Exibe mensagem amigável
- Botão para voltar

### Erro 500 (Erro no Servidor)
- Exibe mensagem genérica
- Log do erro no console
- Opção de tentar novamente

## CORS

Backend precisa ter CORS configurado para aceitar requisições do frontend:

```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Checklist de Integração

- [ ] Backend rodando na porta 8000
- [ ] Frontend rodando na porta 3000
- [ ] CORS configurado no backend
- [ ] Variável `NEXT_PUBLIC_API_URL` configurada
- [ ] Testar cadastro de novo usuário
- [ ] Testar login
- [ ] Testar criação de assessment
- [ ] Testar salvamento de respostas
- [ ] Testar finalização de assessment
- [ ] Testar visualização de resultados
- [ ] Testar download de PDF
- [ ] Testar acesso admin (dashboard e clientes)
- [ ] Testar logout
- [ ] Testar proteção de rotas

## Dicas de Debugging

### Ver requisições no DevTools
1. Abrir DevTools (F12)
2. Aba "Network"
3. Filtrar por "Fetch/XHR"
4. Ver requisições e respostas

### Ver estado do Zustand
Usar extensão do navegador: Redux DevTools (funciona com Zustand)

### Logs úteis
```tsx
// Ver token
console.log(localStorage.getItem('entrepreneur_assessment_token'))

// Ver usuário
console.log(localStorage.getItem('entrepreneur_assessment_user'))

// Ver estado do assessment
console.log(useAssessmentStore.getState())
```

## Produção

### Build do Frontend
```bash
npm run build
npm start
```

### Variáveis de Ambiente em Produção
```bash
NEXT_PUBLIC_API_URL=https://api.seudominio.com
```

### Deploy Sugerido
- Frontend: Vercel / Netlify
- Backend: AWS / Digital Ocean / Heroku
- Database: PostgreSQL managed (AWS RDS / Digital Ocean)
