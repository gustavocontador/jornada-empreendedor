# Frontend - Jornada do Empreendedor de Sucesso

Frontend completo desenvolvido em Next.js 14 (App Router) com TypeScript, Tailwind CSS e shadcn/ui.

## Tecnologias

- **Next.js 14** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes UI (Radix UI)
- **Zustand** - State management
- **React Hook Form + Zod** - Formulários e validação
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones

## Estrutura do Projeto

```
src/
├── app/                          # Páginas (App Router)
│   ├── (auth)/
│   │   ├── login/                # Login
│   │   └── register/             # Cadastro
│   ├── (assessment)/
│   │   ├── questionario/         # Questionário
│   │   └── resultado/[id]/       # Resultados
│   ├── (admin)/
│   │   ├── dashboard/            # Dashboard admin
│   │   └── clientes/             # Lista de clientes
│   ├── layout.tsx                # Layout raiz
│   ├── page.tsx                  # Landing page
│   └── globals.css               # Estilos globais
├── components/
│   ├── ui/                       # Componentes shadcn/ui
│   ├── charts/                   # Gráficos dos frameworks
│   │   ├── DISCChart.tsx
│   │   ├── SpiralChart.tsx
│   │   ├── PAEIChart.tsx
│   │   └── EnneagramChart.tsx
│   └── assessment/               # Componentes do questionário
│       ├── QuestionCard.tsx
│       ├── ProgressBar.tsx
│       └── QuestionNavigation.tsx
├── hooks/
│   ├── useAuth.ts                # Hook de autenticação
│   └── useAssessment.ts          # Hook do assessment
├── stores/
│   ├── authStore.ts              # Estado de autenticação
│   └── assessmentStore.ts        # Estado do assessment
├── lib/
│   ├── api.ts                    # Cliente Axios
│   ├── auth.ts                   # Funções de autenticação
│   └── utils.ts                  # Utilitários
└── types/
    ├── user.ts                   # Types de usuário
    ├── assessment.ts             # Types de assessment
    └── result.ts                 # Types de resultados
```

## Instalação

1. Instalar dependências:
```bash
npm install
```

2. Configurar variáveis de ambiente:
```bash
cp .env.example .env.local
```

Editar `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Rodar em desenvolvimento:
```bash
npm run dev
```

Acesse: http://localhost:3000

## Build para Produção

```bash
npm run build
npm start
```

## Features Implementadas

### Autenticação
- Login com email/senha
- Cadastro de novos usuários
- Proteção de rotas privadas
- JWT token no localStorage
- Refresh automático (interceptor Axios)

### Landing Page
- Hero section atraente
- Seção de benefícios (6 frameworks)
- Como funciona
- CTAs para cadastro

### Questionário
- Progress bar animada
- Renderização de 4 tipos de perguntas:
  - Likert 5 pontos
  - Múltipla escolha
  - Ranking
  - Texto livre
- Auto-save (debounced)
- Navegação anterior/próxima
- Validação antes de avançar

### Resultados
- Tabs para cada framework
- Gráficos visuais:
  - DISC: Barras horizontais
  - Espiral Dinâmica: Radar colorido
  - PAEI: Radar 4 dimensões
  - Eneagrama: Círculo com tipos
- Valores principais
- Recomendações personalizadas
- Download de PDF (integrado com backend)

### Admin
- Dashboard com estatísticas
- Lista de clientes
- Busca/filtro
- Ver resultados de clientes

## Cores dos Frameworks

### Espiral Dinâmica (fiéis ao original)
- Bege: #F5DEB3
- Roxo: #9370DB
- Vermelho: #DC143C
- Azul: #4169E1
- Laranja: #FF8C00
- Verde: #32CD32
- Amarelo: #FFD700
- Turquesa: #40E0D0

### DISC
- D (Dominância): #FF4444
- I (Influência): #FFD700
- S (Estabilidade): #4CAF50
- C (Conformidade): #2196F3

### PAEI
- P (Produtor): #8B4513
- A (Administrador): #2F4F4F
- E (Empreendedor): #FF6347
- I (Integrador): #4682B4

## Integração com Backend

Todas as rotas da API estão integradas:

- POST /api/auth/register
- POST /api/auth/login
- POST /api/assessments
- GET /api/assessments/:id
- GET /api/questions
- POST /api/responses
- POST /api/assessments/:id/complete
- GET /api/results/:id
- GET /api/results/:id/pdf
- GET /api/admin/stats
- GET /api/admin/assessments/recent
- GET /api/admin/clients

## Estado Global

### authStore (Zustand)
- user
- token
- isAuthenticated
- isAdmin
- setAuth()
- logout()
- initAuth()

### assessmentStore (Zustand)
- assessment
- questions
- responses
- currentQuestionIndex
- setAssessment()
- setQuestions()
- setResponse()
- setCurrentQuestionIndex()
- getCurrentQuestion()
- getProgress()
- reset()

## Validação

Todos os formulários usam:
- **react-hook-form** para gerenciamento
- **zod** para schemas de validação
- Mensagens de erro em português
- Validação em tempo real

## Responsividade

Todo o design é responsivo:
- Mobile first
- Breakpoints do Tailwind
- Grid layouts adaptativos
- Componentes flexíveis

## Próximos Passos

1. Testar integração completa com backend
2. Ajustar tipos TypeScript conforme resposta real da API
3. Adicionar loading states em todas as operações assíncronas
4. Implementar error boundaries
5. Adicionar testes (Jest + React Testing Library)

## Scripts Disponíveis

- `npm run dev` - Desenvolvimento
- `npm run build` - Build de produção
- `npm start` - Rodar build
- `npm run lint` - Linter
- `npm run type-check` - Verificar tipos TypeScript
