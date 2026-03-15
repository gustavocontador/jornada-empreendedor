# Epic 7: Setup Monorepo + CI/CD

**ID:** EPIC-007
**Título:** Infraestrutura Base - Turborepo + GitHub Actions + Deploy
**Prioridade:** 🔴 P0 (Bloqueante - Primeiro épico)
**Estimativa:** Medium (4-6 dias, 1 dev + 1 devops)
**Status:** 📋 Backlog

---

## Objetivo

Configurar infraestrutura base com monorepo Turborepo, CI/CD (GitHub Actions), deploy automatizado (Vercel + Railway + Supabase) e observabilidade (Sentry - já implementado).

---

## Business Value

- ✅ **Qualidade desde dia 1** - CI/CD bloqueia merge se testes falharem
- ✅ **Velocidade** - Deploy automatizado em < 5min
- ✅ **Observabilidade** - Sentry ativo desde início
- ✅ **Escalabilidade** - Monorepo permite shared types/utils

---

## Escopo In

1. **Monorepo Turborepo:**
   - Estrutura: `/backend`, `/frontend`, `/shared`
   - Workspaces configurados (package.json root)
   - Shared types TypeScript (backend schemas → frontend)
   - Turborepo cache local + remoto (Vercel)

2. **GitHub Actions CI/CD:**
   - Workflow: `.github/workflows/ci.yml`
   - Jobs paralelos: lint-backend, lint-frontend, test-backend, test-frontend, e2e-tests
   - Quality gates: coverage > 80%, lint pass, typecheck pass
   - Deploy automático: main → production, develop → staging

3. **Deploy Strategy:**
   - **Frontend:** Vercel (Next.js otimizado)
   - **Backend:** Railway (Python FastAPI)
   - **Database:** Supabase (PostgreSQL + RLS)
   - **Storage:** Supabase Storage (PDFs)
   - **Secrets:** Railway Secrets + Vercel Env Vars

4. **Observabilidade (já implementado na Fase 1):**
   - Sentry backend + frontend
   - Structured logging (JSON)
   - Health checks (/health, /health/ready, /health/live)
   - Performance middleware (X-Response-Time)

## User Stories

### US-007.1: Inicializar Monorepo Turborepo
**Como** dev
**Quero** estrutura de monorepo funcional
**Para** compartilhar código entre backend e frontend

**AC:**
- [ ] `npx create-turbo@latest` → estrutura inicial
- [ ] Workspaces: `backend/`, `frontend/`, `shared/`
- [ ] `turbo.json` configurado (pipeline: lint, test, build)
- [ ] `package.json` root com scripts: `turbo run lint`, `turbo run test`
- [ ] Shared types em `shared/types/` (exemplo: UserSchema)
- [ ] Backend importa: `import { UserSchema } from '@jornada/shared'`
- [ ] Frontend importa: `import { UserSchema } from '@jornada/shared'`

### US-007.2: Configurar GitHub Actions CI
**Como** dev
**Quero** CI automatizado que roda testes e lint
**Para** garantir qualidade antes de merge

**AC:**
- [ ] `.github/workflows/ci.yml` criado
- [ ] Jobs paralelos: lint-backend, lint-frontend, test-backend, test-frontend
- [ ] Matrix builds: Python 3.12, Node 20
- [ ] Quality gate: coverage > 80% (fail se não atingir)
- [ ] Quality gate: lint pass (Ruff backend, ESLint frontend)
- [ ] Quality gate: typecheck pass (mypy backend, tsc frontend)
- [ ] PR bloqueado se CI falhar

### US-007.3: Deploy Automatizado
**Como** dev
**Quero** deploy automático ao fazer push na main
**Para** entregar features rapidamente

**AC:**
- [ ] Push em `main` → trigger deploy production
- [ ] Push em `develop` → trigger deploy staging
- [ ] Backend: Railway auto-deploy (via railway.json)
- [ ] Frontend: Vercel auto-deploy (via vercel.json)
- [ ] Database migrations: Supabase auto-migrate (via CLI)
- [ ] Rollback automático se healthcheck falhar

---

## Tech Stack

- **Monorepo:** Turborepo
- **CI/CD:** GitHub Actions
- **Deploy:**
  - Frontend: Vercel
  - Backend: Railway
  - Database: Supabase
- **Observabilidade:**
  - Sentry (backend + frontend)
  - Structured logging (python-json-logger)
  - Health checks (FastAPI endpoints)

---

## Dependências

**Bloqueia:** Todos os outros épicos (1-6)

---

## Métricas de Sucesso

- **CI Runtime:** < 5min (lint + test + typecheck)
- **Deploy Time:** < 3min (main → production)
- **Test Coverage:** > 80%
- **Health Check Uptime:** > 99.9%

---

**Criado por:** @pm (Morgan)
**Data:** 2026-03-15

— Morgan, planejando o futuro 📊
