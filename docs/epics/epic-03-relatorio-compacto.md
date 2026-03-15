# Epic 3: Relatório Compacto Automatizado

**ID:** EPIC-003
**Título:** Geração Automática de Relatório Compacto em PDF (Low Ticket)
**Prioridade:** 🟡 P1 (Alta)
**Estimativa:** Medium (6-8 dias, 1-2 devs)
**Status:** 📋 Backlog
**Owner:** @pm (Morgan)

---

## Objetivo

Gerar automaticamente relatório PDF compacto (8-10 páginas) com gráficos dos 6 frameworks, interpretações automatizadas e plano de ação básico após pagamento de low ticket (R$ 47-97).

---

## Business Value

- ✅ **Produto low ticket** - Entrada acessível para funil de vendas
- ✅ **Entrega imediata** - PDF pronto em < 30s após pagamento
- ✅ **Escalável** - Zero intervenção humana
- ✅ **Upsell** - Gateway para relatório Full

---

## Escopo In

1. **PDF Generation:**
   - WeasyPrint (HTML→PDF) como primário
   - Templates Jinja2 + Tailwind CSS
   - Gráficos: Chart.js renderizado para imagem PNG
   - 8-10 páginas: Capa + 6 frameworks + Plano de Ação + Próximos Passos

2. **Conteúdo Automatizado:**
   - Capa personalizada (nome do usuário)
   - Seção por framework com gráfico radar/bar + texto interpretativo
   - Interpretações baseadas em rules engine (if score > 70: "alto", 50-70: "médio", < 50: "baixo")
   - Plano de ação básico (3-5 sugestões genéricas baseadas em perfil dominante)

3. **Storage & Download:**
   - Upload para Supabase Storage (/compact-reports/{user_id}/{timestamp}.pdf)
   - URL de download com expiração (7 dias)
   - Email com link de download

4. **Payment Integration:**
   - Stripe Checkout session (R$ 47-97)
   - Webhook de confirmação de pagamento
   - Trigger de geração após pagamento confirmado

## User Stories

### US-003.1: Gerar PDF Automaticamente
**Como** sistema
**Quero** gerar PDF do relatório compacto após pagamento
**Para** entregar ao usuário imediatamente

**AC:**
- [ ] Trigger automático após webhook Stripe (payment_intent.succeeded)
- [ ] WeasyPrint gera PDF de template Jinja2
- [ ] Gráficos renderizados como PNG (Chart.js via Puppeteer ou canvas)
- [ ] PDF salvo em Supabase Storage
- [ ] Email enviado com link de download
- [ ] Tempo de geração: < 30s (p95)

### US-003.2: Baixar Relatório Compacto
**Como** usuário que pagou
**Quero** baixar meu relatório compacto
**Para** ler meus resultados

**AC:**
- [ ] Link de download no email (botão "Baixar Relatório")
- [ ] GET /api/v1/reports/compact/{id}/download retorna PDF
- [ ] Verifica pagamento confirmado (status='paid')
- [ ] Verifica ownership (user_id do token = user_id do relatório)
- [ ] Content-Disposition: attachment (força download)
- [ ] Link expira após 7 dias

## Dependências

**É Bloqueado Por:**
- Epic 2 (Assessment) - precisa de scores
- Epic 6 (Pagamentos) - precisa de confirmação de pagamento

---

## Database Schema

```sql
CREATE TABLE compact_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  assessment_id UUID REFERENCES assessments(id),
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'error'
  payment_status VARCHAR(50) DEFAULT 'unpaid', -- 'unpaid', 'paid'
  file_url TEXT,
  generated_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/v1/reports/compact | Cria intent de relatório (pré-pagamento) |
| GET | /api/v1/reports/compact/{id}/download | Baixa PDF |
| POST | /webhooks/stripe | Webhook Stripe (confirma pagamento → trigger geração) |

## Métricas de Sucesso

- **Geração:** < 30s (p95)
- **Taxa de sucesso:** > 98%
- **Taxa de download:** > 90% (24h após email)

---

**Criado por:** @pm (Morgan)
**Data:** 2026-03-15
