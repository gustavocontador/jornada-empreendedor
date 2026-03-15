# Epic 4: Relatório Full com Feedback Humano

**ID:** EPIC-004
**Título:** Relatório Full Personalizado com Análise de Especialista
**Prioridade:** 🟡 P1 (Alta)
**Estimativa:** Medium (7-9 dias, 2 devs)
**Status:** 📋 Backlog

---

## Objetivo

Gerar relatório PDF Full (25-35 páginas) com feedback humano personalizado por especialista após pagamento de ticket alto (R$ 297-697).

---

## Business Value

- ✅ **Produto premium** - Ticket alto (R$ 297-697)
- ✅ **Diferenciação** - Análise humana personalizada
- ✅ **Retenção** - Relacionamento com especialista
- ✅ **Margem alta** - Justifica preço premium

---

## Escopo In

1. **Interface Admin de Edição:**
   - Form com 8 campos de texto (feedback por framework + observações + plano de ação)
   - Rich text editor (Quill.js ou TipTap)
   - Auto-save a cada 30s
   - Status workflow: pending → in_review → completed

2. **PDF Full:**
   - 25-35 páginas: Capa + 6 frameworks detalhados + Análise Integrativa + Plano de Ação Personalizado
   - Feedbacks escritos pelo especialista
   - Assinatura digital do especialista
   - Geração com WeasyPrint (mesmo stack do Compacto)

3. **Fila de Trabalho:**
   - Admin vê lista de relatórios Full aguardando feedback (status=in_review)
   - Filtros: data, usuário, framework pendente
   - Deadline: 7 dias após pagamento

## User Stories

### US-004.1: Especialista Edita Feedbacks
**Como** especialista
**Quero** editar feedbacks personalizados por framework
**Para** entregar valor premium ao usuário

**AC:**
- [ ] GET /api/v1/admin/reports/full (lista relatórios in_review)
- [ ] GET /api/v1/admin/reports/full/{id} (detalhes + scores)
- [ ] PUT /api/v1/admin/reports/full/{id}/feedbacks (salva feedbacks)
- [ ] 8 campos: disc_feedback, spiral_feedback, paei_feedback, enneagram_feedback, values_feedback, archetypes_feedback, general_observations, action_plan
- [ ] Auto-save a cada 30s
- [ ] Indicador: "Salvo às 14:23"

### US-004.2: Gerar PDF Full
**Como** especialista
**Quero** gerar o PDF final após completar feedbacks
**Para** entregar ao usuário

**AC:**
- [ ] Botão "Gerar Relatório Final"
- [ ] Valida: todos 8 campos preenchidos (min 100 chars cada)
- [ ] POST /api/v1/admin/reports/full/{id}/generate
- [ ] WeasyPrint gera PDF (25-35 páginas)
- [ ] Upload para Supabase Storage
- [ ] Email ao usuário: "Seu relatório Full está pronto!"
- [ ] Status: in_review → completed

---

## Database Schema

```sql
CREATE TABLE full_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  assessment_id UUID REFERENCES assessments(id),
  specialist_id UUID REFERENCES users(id),
  status VARCHAR(50) DEFAULT 'pending',
  payment_status VARCHAR(50) DEFAULT 'unpaid',
  feedbacks JSONB, -- {disc_feedback, spiral_feedback, ...}
  file_url TEXT,
  generated_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Dependências

**É Bloqueado Por:** Epic 2, Epic 6

---

**Criado por:** @pm (Morgan)
