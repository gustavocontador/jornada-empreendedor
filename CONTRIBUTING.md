# 🤝 Guia de Contribuição - Jornada do Empreendedor

## 📦 Estrutura do Monorepo

Este projeto utiliza **Turborepo** para gerenciar múltiplos workspaces:

- `backend/` - FastAPI (Python 3.12+)
- `frontend/` - Next.js 15 (TypeScript 5.x strict)
- `shared/` - Tipos TypeScript compartilhados

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
# Na raiz do projeto
npm install
```

Isso instalará todas as dependências de todos os workspaces, incluindo o Turborepo.

### 2. Desenvolvimento

```bash
# Rodar todos os workspaces em modo dev
npm run dev

# Rodar apenas frontend
npx turbo run dev --filter=@jornada/frontend

# Rodar apenas backend
npx turbo run dev --filter=@jornada/backend
```

### 3. Lint e Testes

```bash
# Lint em todos os workspaces
npm run lint

# Build de todos os workspaces
npm run build

# Testes em todos os workspaces
npm run test
```

## 📝 Workflow de Desenvolvimento

### 1. Criar Branch

```bash
git checkout -b feature/sua-feature
```

### 2. Fazer Modificações

- **Frontend:** Editar arquivos em `frontend/src/`
- **Backend:** Editar arquivos em `backend/app/`
- **Tipos compartilhados:** Editar arquivos em `shared/types/`

### 3. Usar Tipos Compartilhados

**No Frontend:**

```typescript
import { UserSchema, AssessmentSchema } from '@jornada/shared';

const user: UserSchema = {
  id: '1',
  email: 'test@example.com',
  full_name: 'Test User',
  role: 'user'
};
```

**No Backend (Python):**

```python
# Python não importa TypeScript diretamente
# Use Pydantic models que espelham os tipos TS
# Exemplo: app/schemas/user.py
```

### 4. Adicionar Novos Tipos Compartilhados

```bash
# Criar novo tipo em shared/types/novo-tipo.ts
# Exportar em shared/index.ts
```

```typescript
// shared/types/novo-tipo.ts
export interface NovoTipo {
  id: string;
  nome: string;
}

// shared/index.ts
export * from './types/novo-tipo';
```

### 5. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/sua-feature
```

## 🏗️ Adicionar Novo Workspace

```bash
# 1. Criar diretório
mkdir novo-workspace

# 2. Criar package.json
cat > novo-workspace/package.json <<EOF
{
  "name": "@jornada/novo-workspace",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "...",
    "build": "...",
    "lint": "...",
    "test": "..."
  }
}
EOF

# 3. Adicionar ao root package.json workspaces array
# "workspaces": ["backend", "frontend", "shared", "novo-workspace"]

# 4. Reinstalar dependências
npm install
```

## 🔧 Turborepo Cache

### Local Cache

O cache local é armazenado em `.turbo/` (gitignored). Ele acelera builds subsequentes reutilizando resultados anteriores.

### Remote Cache (Opcional)

Para compartilhar cache entre desenvolvedores:

```bash
# Login no Vercel
npx turbo login

# Link ao projeto
npx turbo link

# Agora o cache será compartilhado remotamente
```

## 📚 Referências

- [Turborepo Docs](https://turbo.build/repo/docs)
- [Next.js 15 Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## ❓ Dúvidas

Abra uma issue no repositório ou entre em contato com a equipe.
