# Epic 2: Assessment 103 Perguntas + Algoritmos de Scoring

**ID:** EPIC-002
**Título:** Questionário Multi-Framework com Auto-Save e Cálculo de Scores
**Prioridade:** 🔴 P0 (Crítico)
**Estimativa:** Large (10-12 dias, 2 devs)
**Status:** 📋 Backlog
**Owner:** @pm (Morgan)

---

## Objetivo

Implementar fluxo completo de assessment com 103 perguntas divididas em 5 seções, salvamento automático de rascunho, navegação flexível e cálculo paralelo de scores em 6 frameworks psicométricos (DISC, Espiral Dinâmica, PAEI, Eneagrama, Valores Empresariais, Arquétipos).

---

## Business Value

### Para o Usuário:
- ✅ Assessment completo em **30 minutos** (média)
- ✅ **Auto-save** a cada 30s (nunca perde progresso)
- ✅ **Pausar e retomar** em qualquer momento (até 30 dias)
- ✅ **Editar respostas** antes de finalizar
- ✅ **6 perfis integrados** em uma única sessão

### Para o Negócio:
- ✅ **Taxa de conclusão elevada** (auto-save reduz abandono)
- ✅ **Dados ricos** para relatórios (103 respostas + 6 scores)
- ✅ **Escalável** (processamento assíncrono de scores)
- ✅ **Reutilização** do questionário YAML do V1 (103 perguntas validadas)

---

## Escopo

### ✅ In Scope

1. **Carregamento de Perguntas:**
   - Ler `questions/questionario-completo-v1.yaml` (103 perguntas)
   - Endpoint GET /api/v1/questions (retorna perguntas por seção ou todas)
   - Cache em memória (reload apenas ao reiniciar backend)

2. **Fluxo de Resposta:**
   - Criar novo assessment (POST /api/v1/assessments)
   - Exibir perguntas por seção (5 seções: DISC, Espiral, PAEI, Eneagrama, Valores/Arquétipos)
   - Salvar respostas individuais (PUT /api/v1/assessments/{id}/responses)
   - Auto-save a cada 30 segundos (frontend)
   - Navegação: Anterior/Próxima, menu lateral de seções
   - Indicador de progresso (X de 103 respondidas)

3. **Preview e Finalização:**
   - Tela de resumo com todas as respostas
   - Filtro por seção
   - Editar resposta individual
   - Finalizar assessment (irreversível, muda status para "completed")
   - Validação de 103 respostas obrigatórias

4. **Cálculo de Scores (Assíncrono):**
   - Trigger automático ao finalizar assessment
   - 6 calculadores paralelos (tasks assíncronas):
     - DISCCalculator
     - SpiralDynamicsCalculator
     - PAEICalculator
     - EnneagramCalculator
     - ValuesCalculator
     - ArchetypesCalculator
   - Algoritmo: Normalização Likert `(value-3)/2 → [-1,1]`, acumulação ponderada, conversão 0-100
   - Armazenar scores em JSONB (tabela assessments.scores)
   - Tempo de cálculo: < 5s (p95)

5. **Tipos de Perguntas:**
   - **Likert 5 pontos:** Radio buttons horizontais (1=Discordo Totalmente, 5=Concordo Totalmente)
   - **Ranking:** Drag-and-drop para ordenar top 3 (q086 Valores, q087 Arquétipos)

### ❌ Out of Scope (Fase 2)

- Perguntas condicionais (lógica de skip)
- Perguntas abertas de texto (apenas Likert + Ranking no MVP)
- Comparação com benchmarks (outros empreendedores)
- Detecção de respostas inconsistentes (ex: responder tudo 5)
- Exportação de respostas brutas (CSV)

---

## User Stories (Alto Nível)

### US-002.1: Iniciar Assessment
**Como** usuário logado
**Quero** iniciar um novo assessment
**Para** descobrir meu perfil empreendedor

**Critérios de Aceitação:**
- [ ] Botão "Iniciar Assessment" no dashboard
- [ ] POST /api/v1/assessments cria novo assessment (status: draft)
- [ ] Associa assessment ao user_id do usuário logado
- [ ] Retorna assessment_id
- [ ] Redirect para primeira pergunta (seção DISC, q001)

---

### US-002.2: Responder Perguntas com Auto-Save
**Como** usuário respondendo o assessment
**Quero** que minhas respostas sejam salvas automaticamente
**Para** não perder progresso se sair da página

**Critérios de Aceitação:**
- [ ] Ao selecionar resposta Likert, salva automaticamente após 30s sem mudança
- [ ] Indicador visual: "Salvando..." → "Salvo às 14:23"
- [ ] PUT /api/v1/assessments/{id}/responses (body: {question_id, value})
- [ ] Backend valida: question_id existe, value válido (1-5 para Likert)
- [ ] Se offline: armazena em localStorage, sincroniza ao voltar online
- [ ] Se navegador fechar: ao reabrir, retoma de onde parou

---

### US-002.3: Navegar Entre Perguntas
**Como** usuário respondendo
**Quero** voltar e revisar respostas anteriores
**Para** garantir que respondi corretamente

**Critérios de Aceitação:**
- [ ] Botão "Anterior" (desabilitado na primeira pergunta)
- [ ] Botão "Próxima" (desabilitado se resposta obrigatória não preenchida)
- [ ] Menu lateral com 5 seções (indicador: completa ✓, incompleta ⏳)
- [ ] Clicar em seção: vai para primeira pergunta não respondida daquela seção
- [ ] Indicador de progresso: "42 de 103 perguntas respondidas (41%)"

---

### US-002.4: Preview de Respostas Antes de Finalizar
**Como** usuário que terminou de responder
**Quero** revisar todas minhas respostas antes de finalizar
**Para** corrigir erros

**Critérios de Aceitação:**
- [ ] Após responder 103 perguntas: botão "Revisar Respostas"
- [ ] Tela de resumo com todas as respostas agrupadas por seção
- [ ] Cada resposta exibe: pergunta, resposta selecionada
- [ ] Botão "Editar" ao lado de cada resposta (volta para aquela pergunta)
- [ ] Filtro por seção (dropdown)
- [ ] Botão "Finalizar Assessment" (destacado, vermelho)
- [ ] Modal de confirmação: "Após finalizar, não será possível editar. Deseja continuar?"

---

### US-002.5: Finalizar Assessment e Calcular Scores
**Como** usuário que revisou as respostas
**Quero** finalizar o assessment
**Para** receber meu relatório

**Critérios de Aceitação:**
- [ ] Botão "Finalizar Assessment" (apenas se 103 respostas completas)
- [ ] Modal de confirmação (duplo opt-in)
- [ ] POST /api/v1/assessments/{id}/submit
- [ ] Backend valida: 103 respostas obrigatórias preenchidas
- [ ] Muda status: draft → completed
- [ ] Timestamp: completed_at
- [ ] Trigger assíncrono: `calculate_scores_task.delay(assessment_id)`
- [ ] Frontend redireciona para tela "Processando..." (loading)
- [ ] Polling a cada 2s: GET /api/v1/assessments/{id}/scores/status
- [ ] Quando scores prontos: redirect para página de resultados

---

### US-002.6: Cálculo de Scores (Backend)
**Como** sistema
**Quero** calcular scores de 6 frameworks em paralelo
**Para** gerar relatórios rapidamente

**Critérios de Aceitação:**
- [ ] ScoringEngine orquestra 6 calculadores
- [ ] Cada calculador é uma task assíncrona (Celery ou FastAPI BackgroundTasks)
- [ ] Algoritmo de normalização: `(value-3)/2` para Likert 1-5 → [-1, 1]
- [ ] Acumulação ponderada por framework (pesos do knowledge base)
- [ ] Conversão final para escala 0-100: `(score_normalizado + 1) * 50`
- [ ] Armazena em assessments.scores (JSONB):
  ```json
  {
    "disc": {"D": 75, "I": 60, "S": 45, "C": 80},
    "spiral_dynamics": {"beige": 10, "purple": 20, ..., "turquoise": 60},
    "paei": {"P": 70, "A": 65, "E": 80, "I": 55},
    "enneagram": {"type_1": 40, "type_2": 30, ..., "type_9": 70},
    "values": {"inovacao": 85, "estabilidade": 30, ...},
    "archetypes": {"criador": 90, "sabio": 60, ...}
  }
  ```
- [ ] Tempo de processamento: < 5s (p95)
- [ ] Erro handling: se falha em 1 calculador, marca como "partial_scores", continua demais

---

## Critérios de Aceitação do Epic

### Técnicos

- [ ] **YAML Loader:** Carrega questionario-completo-v1.yaml na inicialização
- [ ] **Auto-Save:** Frontend salva a cada 30s (debounce)
- [ ] **Offline Support:** LocalStorage sync quando voltar online
- [ ] **Processamento Assíncrono:** Scores calculados em background (não bloqueia)
- [ ] **Validação:** 103 respostas obrigatórias antes de finalizar
- [ ] **Test Coverage:** 80%+ (unit + integration)
- [ ] **Performance:** Cálculo de scores em < 5s (p95)

### Funcionais

- [ ] Usuário consegue responder 103 perguntas
- [ ] Auto-save funciona (teste: fechar navegador, reabrir, continuar)
- [ ] Preview de respostas exibe todas as 103 respostas
- [ ] Finalização marca assessment como "completed"
- [ ] Scores calculados corretamente para 6 frameworks
- [ ] Resultados aparecem na tela de resultados

### UX

- [ ] Indicador de progresso claro (X de 103)
- [ ] Navegação intuitiva (Anterior/Próxima/Menu Lateral)
- [ ] Feedback visual de auto-save ("Salvo às 14:23")
- [ ] Loading state durante cálculo de scores (não tela branca)

---

## Dependências

### Bloqueia

- ✅ **Epic 3:** Relatório Compacto (precisa de scores calculados)
- ✅ **Epic 4:** Relatório Full (precisa de scores calculados)

### É Bloqueado Por

- ⚠️ **Epic 1:** Autenticação (precisa de user_id para criar assessment)
- ⚠️ **Epic 7:** Setup Monorepo (precisa de estrutura base)

---

## Tech Stack

### Backend (Python)

- **FastAPI 0.115+**
- **SQLAlchemy 2.x async**
- **PyYAML:** Leitura do questionario-completo-v1.yaml
- **Celery / FastAPI BackgroundTasks:** Processamento assíncrono de scores
- **Redis:** Cache de perguntas (opcional, para performance)

### Frontend (TypeScript)

- **Next.js 15+ App Router**
- **Zustand:** State management (assessmentStore)
- **React Hook Form:** Formulários
- **React Beautiful DnD:** Drag-and-drop para ranking
- **LocalStorage:** Offline sync

### Algoritmo de Scoring

**Linguagem:** Python (ScoringEngine)

**Entrada:** 103 respostas (question_id → value)

**Saída:** 6 objetos JSON com scores 0-100

**Passos:**
1. Normalizar Likert: `(value - 3) / 2` → [-1, 1]
2. Acumular ponderado: `raw_scores[key] += normalized * weight`
3. Média: `avg_score = raw_scores[key] / question_count[key]`
4. Converter 0-100: `(avg_score + 1) * 50`

---

## Database Schema

```sql
-- Tabela assessments
CREATE TABLE assessments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'completed'
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  scores JSONB, -- Scores calculados (6 frameworks)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela responses
CREATE TABLE responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
  question_id VARCHAR(10) NOT NULL, -- 'q001', 'q002', etc.
  value INTEGER, -- Para Likert: 1-5
  ranking JSON, -- Para ranking: ["valor1", "valor2", "valor3"]
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(assessment_id, question_id)
);

-- RLS Policies
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE responses ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_assessments ON assessments
  FOR ALL USING (
    user_id = current_user_id() OR
    EXISTS (SELECT 1 FROM users WHERE id = current_user_id() AND role IN ('admin', 'specialist'))
  );

CREATE POLICY user_responses ON responses
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM assessments
      WHERE assessments.id = responses.assessment_id
      AND (assessments.user_id = current_user_id() OR EXISTS (SELECT 1 FROM users WHERE id = current_user_id() AND role IN ('admin', 'specialist')))
    )
  );
```

---

## API Endpoints

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | /api/v1/questions | Lista todas as perguntas (ou por seção) | JWT |
| POST | /api/v1/assessments | Cria novo assessment | JWT |
| GET | /api/v1/assessments/{id} | Detalhes do assessment | JWT |
| PUT | /api/v1/assessments/{id}/responses | Salva resposta (auto-save) | JWT |
| GET | /api/v1/assessments/{id}/responses | Lista todas as respostas | JWT |
| POST | /api/v1/assessments/{id}/submit | Finaliza e calcula scores | JWT |
| GET | /api/v1/assessments/{id}/scores | Retorna scores (se prontos) | JWT |
| GET | /api/v1/assessments/{id}/scores/status | Status do cálculo (pending, processing, completed) | JWT |

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **YAML corrompido** | Baixa | Alto | Validação de schema no startup + backup do YAML |
| **Cálculo de scores lento (>10s)** | Média | Médio | Processamento assíncrono + feedback de loading |
| **Auto-save falha (offline)** | Alta | Baixo | LocalStorage backup + sync ao voltar online |
| **Usuário abandona no meio** | Alta | Médio | Auto-save reduz perda de progresso + email de retomada |
| **Respostas inconsistentes** | Média | Baixo | Validação básica (todos 5 ou todos 1 = alerta) |

---

## Testes Críticos

### Unit Tests

- [ ] YAML loader: carrega 103 perguntas corretamente
- [ ] Normalização Likert: (3-3)/2 = 0, (5-3)/2 = 1, (1-3)/2 = -1
- [ ] Acumulação ponderada: testa com mock responses
- [ ] Conversão 0-100: (-1+1)*50 = 0, (0+1)*50 = 50, (1+1)*50 = 100

### Integration Tests

- [ ] Fluxo completo: create assessment → save responses → submit → calculate scores
- [ ] Auto-save: simula salvamento a cada 30s
- [ ] Finalização com < 103 respostas: retorna erro 422
- [ ] Cálculo paralelo: 6 calculadores executam sem race condition

### E2E Tests (Playwright)

- [ ] Usuário responde assessment completo (103 perguntas)
- [ ] Auto-save: fecha navegador, reabre, continua de onde parou
- [ ] Preview: edita resposta, volta para preview, confirma alteração
- [ ] Finaliza: aguarda cálculo de scores, vê resultados

---

## Métricas de Sucesso

### Técnicas

- **Test Coverage:** 80%+
- **Performance Cálculo:** < 5s (p95)
- **Auto-Save Success Rate:** > 99.5%

### Funcionais

- **Taxa de conclusão:** > 70% (dos que iniciam, finalizam)
- **Tempo médio de resposta:** 25-35 minutos
- **Taxa de edição de respostas:** < 5% (após preview)

### UX

- **NPS (ease of use):** > 8/10
- **Abandono por frustração:** < 5%

---

## Handoff para @sm (Story Creation)

**Próximo passo:** @sm cria stories detalhadas para cada US.

**Priorização:** US-002.1 (Iniciar) → US-002.2 (Responder + Auto-Save) → US-002.3 (Navegação) → US-002.6 (Cálculo Scores) → US-002.4 (Preview) → US-002.5 (Finalizar)

---

**Criado por:** @pm (Morgan)
**Data:** 2026-03-15
**Versão:** 1.0.0

— Morgan, planejando o futuro 📊
