# Epic 6: Pagamentos Stripe

**ID:** EPIC-006
**Título:** Integração Stripe para Relatórios Compacto e Full
**Prioridade:** 🔴 P0 (Crítico para monetização)
**Estimativa:** Medium (5-7 dias, 1 dev)
**Status:** 📋 Backlog

---

## Objetivo

Integrar Stripe Checkout para venda de Relatório Compacto (R$ 47-97) e Relatório Full (R$ 297-697).

---

## Business Value

- ✅ **Monetização** - Receita desde o MVP
- ✅ **Automatização** - Pagamentos sem intervenção humana
- ✅ **Segurança** - PCI compliance via Stripe
- ✅ **Conversão** - Checkout otimizado

---

## Escopo In

1. **Stripe Checkout Session:**
   - Criar sessão de checkout (POST /api/v1/payments/checkout)
   - Produtos: "Relatório Compacto" (R$ 47-97), "Relatório Full" (R$ 297-697)
   - Redirect success: /pagamento-confirmado
   - Redirect cancel: /pagamento-cancelado

2. **Webhooks:**
   - /webhooks/stripe (POST)
   - Eventos: payment_intent.succeeded, checkout.session.completed
   - Atualizar payment_status: unpaid → paid
   - Trigger geração de relatório (Compacto imediato, Full entra na fila)

3. **Frontend:**
   - Botões "Comprar Relatório Compacto" / "Comprar Relatório Full"
   - Redirect para Stripe Checkout
   - Página de confirmação (/pagamento-confirmado)
   - Loading enquanto aguarda geração do PDF

## User Stories

### US-006.1: Usuário Compra Relatório Compacto
**Como** usuário que finalizou assessment
**Quero** comprar o relatório compacto
**Para** receber meus resultados

**AC:**
- [ ] Botão "Comprar Relatório Compacto (R$ 47)"
- [ ] POST /api/v1/payments/checkout (body: {product: "compact", assessment_id})
- [ ] Retorna: checkout_url
- [ ] Redirect para Stripe Checkout
- [ ] Preenche dados de cartão
- [ ] Pagamento aprovado → redirect /pagamento-confirmado
- [ ] Webhook atualiza payment_status=paid
- [ ] Trigger geração de PDF
- [ ] Email: "Seu relatório está sendo gerado..."
- [ ] Após geração: Email com link de download

### US-006.2: Webhook Confirma Pagamento
**Como** sistema
**Quero** receber confirmação do Stripe via webhook
**Para** liberar relatório automaticamente

**AC:**
- [ ] POST /webhooks/stripe (Stripe-Signature header)
- [ ] Verifica assinatura (webhook secret)
- [ ] Evento payment_intent.succeeded:
  - [ ] Busca compact_report ou full_report por payment_intent_id
  - [ ] Atualiza payment_status=paid
  - [ ] Se Compacto: trigger generate_compact_report_task.delay(report_id)
  - [ ] Se Full: update status=in_review (entra na fila de especialista)
- [ ] Retorna 200 OK para Stripe

---

## Database Schema

```sql
ALTER TABLE compact_reports ADD COLUMN payment_intent_id VARCHAR(255);
ALTER TABLE full_reports ADD COLUMN payment_intent_id VARCHAR(255);
```

## Stripe Products

- **Relatório Compacto:** R$ 47 (ou R$ 97 com desconto)
- **Relatório Full:** R$ 297 (ou R$ 697 com análise premium)

---

**Criado por:** @pm (Morgan)
