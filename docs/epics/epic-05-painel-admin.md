# Epic 5: Painel Admin

**ID:** EPIC-005
**Título:** Dashboard Administrativo com Gestão de Participantes
**Prioridade:** 🟡 P1 (Alta)
**Estimativa:** Medium (6-8 dias, 1-2 devs)
**Status:** 📋 Backlog

---

## Objetivo

Painel admin para visualizar TODOS os participantes, gráficos inline, status de assessments/relatórios e links de download.

---

## Business Value

- ✅ **Gestão centralizada** - Todos os dados em um lugar
- ✅ **Acompanhamento** - Status de cada participante
- ✅ **Suporte** - Admin pode ver gráficos e ajudar usuários
- ✅ **Controle** - Gerenciar acessos (admin, specialist)

---

## Escopo In

1. **Lista de Participantes:**
   - Tabela com colunas: Nome, Email, Data Cadastro, Status Assessment, Status Compacto, Status Full
   - Filtros: nome, email, status
   - Paginação (50/página)
   - Ordenação por coluna

2. **Gráficos Inline:**
   - Clicar em participante → abre modal com 6 gráficos (radar/bar charts)
   - Dados dos scores do assessment
   - Download de gráfico como PNG

3. **Download de Relatórios:**
   - Link "Baixar Compacto" (se payment_status=paid)
   - Link "Baixar Full" (se status=completed)
   - Links diretos para Supabase Storage

4. **Gestão de Usuários:**
   - Promover usuário para admin/specialist
   - Desativar conta
   - Ver histórico de assessments

## User Stories

### US-005.1: Admin Visualiza Lista de Participantes
**Como** admin
**Quero** ver lista completa de todos os participantes
**Para** gerenciar a plataforma

**AC:**
- [ ] GET /api/v1/admin/participantes (requer role=admin)
- [ ] Retorna: user_id, name, email, created_at, assessment {status, completed_at}, reports {compact, full}
- [ ] Filtros: nome (busca parcial), email, status assessment
- [ ] Paginação: limit=50, offset
- [ ] Ordenação: created_at DESC (default)

### US-005.2: Admin Vê Gráficos de Participante
**Como** admin
**Quero** visualizar gráficos de scores inline
**Para** entender perfil do participante

**AC:**
- [ ] Botão "Ver Gráficos" em cada linha da tabela
- [ ] GET /api/v1/admin/participantes/{user_id}/graficos
- [ ] Modal com 6 gráficos (Chart.js)
- [ ] Botão "Baixar como PNG" em cada gráfico

---

## Dependências

**É Bloqueado Por:** Epic 1 (RLS policies para admin), Epic 2 (scores)

---

**Criado por:** @pm (Morgan)
