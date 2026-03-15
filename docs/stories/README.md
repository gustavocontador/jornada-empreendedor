# Stories - Sistema V2 "Jornada do Empreendedor"

**Scrum Master:** @sm (River)
**Data de Criação:** 2026-03-15
**Baseado em:** Epic 7 (EPIC-007)

---

## Índice de Stories

### Epic 7: Setup Monorepo + CI/CD

| ID | Título | Estimativa | Status | Executor | Dependências |
|----|--------|-----------|--------|----------|--------------|
| [7.1](./7.1.setup-monorepo-turborepo.md) | Setup Monorepo Turborepo | 2 dias | ✅ Approved | @devops | - |
| [7.2](./7.2.github-actions-ci.md) | GitHub Actions CI Pipeline | 2-3 dias | ✅ Approved | @devops | 7.1 |
| [7.3](./7.3.deploy-automatizado.md) | Deploy Automatizado | 2-3 dias | ✅ Approved | @devops | 7.1, 7.2 |

**Total Epic 7:** 6-8 dias (sequencial) | 4-6 dias (com paralelização)

---

## Sprint 0: Infraestrutura (Semana 1)

### Sequência de Execução

```
Dia 1-2: Story 7.1 (Turborepo)
├── Inicializar monorepo
├── Configurar workspaces
├── Criar shared types
└── Validar importações cross-workspace

Dia 2-4: Story 7.2 (CI) [pode começar em paralelo com 7.1 final]
├── Criar workflow CI
├── Configurar jobs paralelos
├── Configurar quality gates
└── Testar branch protection

Dia 4-6: Story 7.3 (Deploy) [depende de 7.1 e 7.2]
├── Setup Vercel (frontend)
├── Setup Railway (backend)
├── Setup Supabase (database)
└── Validar deploy end-to-end
```

---

## Critérios de Aceitação do Epic 7

### Infraestrutura Completa

- [ ] **Monorepo funcionando** (Story 7.1 completa)
  - Turborepo com workspaces backend/frontend/shared
  - Shared types sendo importados corretamente
  - Cache Turborepo ativo

- [ ] **CI/CD ativo** (Story 7.2 completa)
  - GitHub Actions rodando em todos os PRs
  - Quality gates bloqueando merges (coverage < 80%, lint fail)
  - Branch protection configurado

- [ ] **Deploy automatizado** (Story 7.3 completa)
  - Push na main → deploy production (< 3min)
  - Health checks validando deploy
  - Rollback automático se falhar

### Métricas de Sucesso

- **CI Runtime:** < 5min (lint + test + typecheck)
- **Deploy Time:** < 3min (main → production)
- **Test Coverage:** > 80% (enforced por CI)
- **Uptime:** > 99.9% (health checks)

---

## Próximos Steps

### 1. Validação das Stories (@po)

**Próximo passo:** @po (Pax) validar stories usando `*validate-story-draft`

**Checklist de validação (10 pontos):**
1. Story clara com formato "As a, I want, so that"?
2. Critérios de aceitação mensuráveis?
3. Tasks granulares (implementável)?
4. Estimativa realista (1-3 dias)?
5. Executor correto atribuído?
6. Dependências mapeadas?
7. Dev Notes com contexto suficiente?
8. Testing standards definidos?
9. CodeRabbit Integration configurado?
10. Alinhado com PRD e arquitetura?

### 2. Início de Desenvolvimento (@devops)

**Após validação:**
1. @devops pega Story 7.1 (primeira da fila)
2. Cria branch: `git checkout -b feature/7.1-setup-monorepo`
3. Implementa seguindo tasks/subtasks
4. Marca checkboxes conforme completa
5. Atualiza Dev Agent Record (files modified, completion notes)
6. Roda testes e validações
7. Marca story como "Ready for Review"
8. Notifica @github-devops para push e PR

### 3. Épicos Restantes

**Após Epic 7 completo:**
- **Epic 1:** Autenticação JWT + RLS (@sm cria stories)
- **Epic 2:** Assessment 103 Perguntas (@sm cria stories)
- **Epic 6:** Pagamentos Stripe (@sm cria stories)
- **Epic 3:** Relatório Compacto (@sm cria stories)
- **Epic 4 & 5:** Relatório Full + Admin (pós-MVP)

---

## Story Status Legend

| Status | Significado |
|--------|-------------|
| 📋 Draft | Story criada, aguardando validação |
| ✅ Approved | Validada por @po, pronta para dev |
| 🚧 InProgress | Em desenvolvimento por executor |
| 👀 Review | Aguardando code review |
| ✅ Done | Completa, merged na main |

---

## Templates e Checklists

### Story Draft Checklist

Execute `*story-checklist` para validar story antes de handoff:

- [ ] Story tem formato correto (As a, I want, so that)
- [ ] AC numerados e mensuráveis
- [ ] Tasks granulares (< 4h cada)
- [ ] Estimativa baseada em complexity
- [ ] Executor atribuído corretamente
- [ ] Quality gate definido
- [ ] Dev Notes com contexto suficiente
- [ ] Testing standards documentados
- [ ] CodeRabbit integration configurado
- [ ] Change log iniciado

---

## Handoff para @devops

**Executor:** @devops (Gage)
**Starting Point:** Story 7.1 (Turborepo)

**Context Provided:**
- PRD v2.1.0 com requisitos completos
- Arquitetura Part 1-3 com tech stack e patterns
- Fase 1 (Observabilidade) já implementada
- Epic 7 com objetivos e escopo claro
- 3 stories detalhadas com AC técnicos

**Expected Workflow:**
1. Ler Story 7.1 completamente
2. Criar feature branch
3. Implementar tasks sequencialmente
4. Atualizar checkboxes (Dev Agent Record)
5. Executar validações (lint, build, cache test)
6. Marcar "Ready for Review"
7. Handoff para @github-devops (push + PR)

---

**Criado por:** @sm (River)
**Data:** 2026-03-15
**Versão:** 1.0.0

— River, removendo obstáculos 🌊
