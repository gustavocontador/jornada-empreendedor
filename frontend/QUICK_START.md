# Quick Start - Frontend

## Instalação Rápida

```bash
# 1. Instalar dependências
npm install

# 2. Configurar ambiente
cp .env.example .env.local

# 3. Rodar em desenvolvimento
npm run dev
```

Acesse: http://localhost:3000

## Estrutura de Arquivos (Resumo)

```
frontend/
├── src/
│   ├── app/                    # Páginas (App Router)
│   │   ├── page.tsx            # Landing page
│   │   ├── (auth)/             # Login/Register
│   │   ├── (assessment)/       # Questionário/Resultado
│   │   └── (admin)/            # Dashboard/Clientes
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── charts/             # Gráficos (DISC, Spiral, etc.)
│   │   └── assessment/         # Questionário components
│   ├── hooks/                  # useAuth, useAssessment
│   ├── stores/                 # Zustand (authStore, assessmentStore)
│   ├── lib/                    # api, auth, utils
│   └── types/                  # TypeScript types
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Páginas Principais

| Rota | Descrição | Proteção |
|------|-----------|----------|
| `/` | Landing page | Pública |
| `/login` | Login | Pública |
| `/register` | Cadastro | Pública |
| `/questionario` | Questionário | Autenticada |
| `/resultado/[id]` | Resultados | Autenticada |
| `/dashboard` | Dashboard Admin | Admin |
| `/clientes` | Lista Clientes | Admin |

## Componentes Principais

### Gráficos
- `DISCChart` - Barras DISC
- `SpiralChart` - Radar colorido Espiral Dinâmica
- `PAEIChart` - Radar PAEI
- `EnneagramChart` - Círculo Eneagrama
- `ValuesChart` - Top valores

### Assessment
- `QuestionCard` - Renderiza pergunta
- `ProgressBar` - Barra de progresso
- `QuestionNavigation` - Navegação

### UI
- Todos os componentes do shadcn/ui (Button, Input, Card, etc.)

## Hooks Customizados

### useAuth
```tsx
const { user, isAuthenticated, login, logout } = useAuth()

// Login
await login({ email, password })

// Logout
logout()
```

### useAssessment
```tsx
const {
  currentQuestion,
  responses,
  answerQuestion,
  nextQuestion,
  completeAssessment
} = useAssessment()

// Responder pergunta
answerQuestion(questionId, response)

// Avançar
nextQuestion()

// Finalizar
await completeAssessment()
```

## API Integration

Base URL configurada em `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Cliente Axios está em `src/lib/api.ts` com:
- Auto-inject de token JWT
- Interceptor para erro 401
- Redirect automático se não autenticado

## Tecnologias

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** (Radix UI)
- **Zustand** (State)
- **React Hook Form + Zod** (Forms)
- **Axios** (HTTP)

## Scripts

```bash
npm run dev        # Desenvolvimento
npm run build      # Build produção
npm start          # Rodar build
npm run lint       # Linter
npm run type-check # Verificar tipos
```

## Próximos Passos

1. Rodar backend: `cd ../backend && uvicorn app.main:app --reload`
2. Rodar frontend: `npm run dev`
3. Acessar: http://localhost:3000
4. Criar conta
5. Responder questionário
6. Ver resultados

## Suporte

- README.md - Documentação completa
- COMPONENTS.md - Documentação de componentes
- INTEGRATION.md - Guia de integração com backend

---

**Desenvolvido para "Jornada do Empreendedor de Sucesso"**
