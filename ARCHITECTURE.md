# ARQUITETURA - Jornada do Empreendedor de Sucesso

## VISÃO GERAL

Sistema completo de assessment comportamental para empreendedores com:
- 6 frameworks integrados (DISC, Espiral Dinâmica, Valores, PAEI, Eneagrama, Arquétipos)
- ~100-105 perguntas otimizadas
- 2 níveis de relatório (Simplificado 2-3 páginas + Completo 15-20 páginas)
- UX Premium com gráficos coloridos
- Backend Python + Frontend Next.js

---

## STACK TECNOLÓGICA

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 15+
- **Authentication:** JWT (python-jose)
- **PDF Generation:** WeasyPrint + ReportLab
- **Charts:** Plotly Python
- **Validation:** Pydantic v2
- **Testing:** Pytest

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS + shadcn/ui
- **Charts:** Recharts + D3.js
- **Forms:** React Hook Form + Zod
- **State:** Zustand
- **HTTP:** Axios
- **Testing:** Vitest + Testing Library

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Vercel (Frontend) + Railway/Render (Backend)
- **Monitoring:** Sentry

---

## ESTRUTURA DE PASTAS

```
jornada-empreendedor/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── assessments.py
│   │   │   │   │   ├── questions.py
│   │   │   │   │   ├── responses.py
│   │   │   │   │   ├── reports.py
│   │   │   │   │   └── admin.py
│   │   │   │   └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── assessment.py
│   │   │   ├── question.py
│   │   │   ├── response.py
│   │   │   └── result.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── assessment.py
│   │   │   └── report.py
│   │   ├── services/
│   │   │   ├── frameworks/
│   │   │   │   ├── disc.py
│   │   │   │   ├── spiral_dynamics.py
│   │   │   │   ├── valores.py
│   │   │   │   ├── paei.py
│   │   │   │   ├── eneagrama.py
│   │   │   │   └── arquetipos.py
│   │   │   ├── calculators/
│   │   │   │   ├── scoring_engine.py
│   │   │   │   ├── combinations.py
│   │   │   │   └── interpretations.py
│   │   │   ├── reports/
│   │   │   │   ├── report_generator.py
│   │   │   │   ├── simplified_report.py
│   │   │   │   ├── complete_report.py
│   │   │   │   └── templates/
│   │   │   └── auth_service.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── utils/
│   │   │   ├── pdf_utils.py
│   │   │   ├── chart_utils.py
│   │   │   └── validators.py
│   │   └── main.py
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── (assessment)/
│   │   │   │   ├── questionario/
│   │   │   │   └── resultado/
│   │   │   ├── (admin)/
│   │   │   │   ├── dashboard/
│   │   │   │   └── clientes/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── ...
│   │   │   ├── assessment/
│   │   │   │   ├── QuestionCard.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   └── QuestionNavigation.tsx
│   │   │   ├── charts/
│   │   │   │   ├── SpiralChart.tsx
│   │   │   │   ├── DISCChart.tsx
│   │   │   │   ├── PAEIChart.tsx
│   │   │   │   └── EnneagramChart.tsx
│   │   │   └── reports/
│   │   │       ├── SimplifiedReport.tsx
│   │   │       └── CompleteReport.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useAssessment.ts
│   │   │   └── useReports.ts
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   └── assessmentStore.ts
│   │   ├── types/
│   │   │   ├── assessment.ts
│   │   │   ├── user.ts
│   │   │   └── report.ts
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
│
├── docs/
│   ├── api/
│   ├── user-guide/
│   └── admin-guide/
│
├── docker-compose.yml
└── README.md
```

---

## MODELAGEM DO BANCO DE DADOS

### Tabelas Principais

#### `users`
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

#### `assessments`
```sql
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    status VARCHAR(50) DEFAULT 'in_progress', -- in_progress, completed, abandoned
    current_question_index INT DEFAULT 0,
    total_questions INT DEFAULT 105,
    metadata JSONB, -- store additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assessments_user_id ON assessments(user_id);
CREATE INDEX idx_assessments_status ON assessments(status);
```

#### `questions`
```sql
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- likert_5, multiple_choice, ranking
    section VARCHAR(100), -- disc, spiral, valores, paei, eneagrama, arquetipos
    order_index INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB, -- options, scoring rules, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_section ON questions(section);
CREATE INDEX idx_questions_order ON questions(order_index);
```

#### `responses`
```sql
CREATE TABLE responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id),
    answer_value JSONB NOT NULL, -- flexible to store different answer types
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_responses_assessment_id ON responses(assessment_id);
CREATE INDEX idx_responses_question_id ON responses(question_id);
```

#### `results`
```sql
CREATE TABLE results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),

    -- DISC Scores
    disc_d DECIMAL(5,2),
    disc_i DECIMAL(5,2),
    disc_s DECIMAL(5,2),
    disc_c DECIMAL(5,2),
    disc_profile VARCHAR(10), -- Ex: DI, SC, etc.

    -- Espiral Dinâmica Scores
    spiral_beige DECIMAL(5,2),
    spiral_purple DECIMAL(5,2),
    spiral_red DECIMAL(5,2),
    spiral_blue DECIMAL(5,2),
    spiral_orange DECIMAL(5,2),
    spiral_green DECIMAL(5,2),
    spiral_yellow DECIMAL(5,2),
    spiral_turquoise DECIMAL(5,2),
    spiral_primary VARCHAR(20),
    spiral_secondary VARCHAR(20),
    spiral_tertiary VARCHAR(20),

    -- PAEI Scores
    paei_p DECIMAL(5,2),
    paei_a DECIMAL(5,2),
    paei_e DECIMAL(5,2),
    paei_i DECIMAL(5,2),
    paei_code VARCHAR(10), -- Ex: PaEi, PAeI

    -- Eneagrama
    enneagram_type INT, -- 1-9
    enneagram_wing VARCHAR(10), -- Ex: 3w2, 8w7
    enneagram_subtype VARCHAR(20), -- sp, so, sx

    -- Valores Empresariais (top 3)
    valores_primary VARCHAR(100),
    valores_secondary VARCHAR(100),
    valores_tertiary VARCHAR(100),

    -- Arquétipos (perfil ideal de contratação)
    arquetipos JSONB,

    -- Metadata e Interpretações
    interpretations JSONB, -- análises profundas geradas
    recommendations JSONB, -- recomendações personalizadas

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_results_assessment_id ON results(assessment_id);
CREATE INDEX idx_results_user_id ON results(user_id);
```

#### `reports`
```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID REFERENCES results(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    report_type VARCHAR(50) NOT NULL, -- simplified, complete
    pdf_path VARCHAR(500), -- path to generated PDF
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_reports_result_id ON reports(result_id);
CREATE INDEX idx_reports_user_id ON reports(user_id);
```

---

## FLUXO DE DADOS

### 1. Cadastro e Autenticação
```
User → POST /api/v1/auth/register → Create User → Return JWT
User → POST /api/v1/auth/login → Validate Credentials → Return JWT
```

### 2. Iniciar Assessment
```
User → POST /api/v1/assessments/start → Create Assessment Record → Return Assessment ID
```

### 3. Responder Perguntas
```
User → GET /api/v1/questions?assessment_id={id} → Return Questions Paginated
User → POST /api/v1/responses → Save Response → Update Progress
```

### 4. Finalizar Assessment e Calcular Resultados
```
User → POST /api/v1/assessments/{id}/complete
  ↓
Scoring Engine:
  1. Load All Responses
  2. Calculate DISC scores
  3. Calculate Espiral scores
  4. Calculate PAEI scores
  5. Calculate Eneagrama scores
  6. Calculate Valores ranking
  7. Analyze Arquetipos preferences
  8. Generate Interpretations (using Spiral Dynamics knowledge base)
  9. Generate Recommendations
  ↓
Save to results table
  ↓
Return Results Summary
```

### 5. Gerar Relatórios
```
User → POST /api/v1/reports/generate
  ↓
Report Generator:
  1. Load Results
  2. Load Spiral Dynamics Knowledge Base
  3. Generate Charts (Plotly)
  4. Apply Templates (Simplified or Complete)
  5. Render PDF (WeasyPrint)
  6. Save PDF to storage
  ↓
Return PDF Download Link
```

---

## ALGORITMOS DE CÁLCULO

### 1. DISC Scoring

```python
def calculate_disc(responses: List[Response]) -> DISCResult:
    """
    Calcula scores DISC baseado nas respostas.
    Perguntas DISC usam escala Likert 1-5.
    """
    disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0}

    # Mapear perguntas para dimensões DISC
    for response in responses:
        question = response.question
        if question.section == "disc":
            # Cada pergunta pode pontuar para múltiplas dimensões
            scoring_rules = question.metadata["scoring"]
            value = response.answer_value["value"]

            for dimension, weight in scoring_rules.items():
                disc_scores[dimension] += value * weight

    # Normalizar para escala 0-10
    max_score = max(disc_scores.values())
    for key in disc_scores:
        disc_scores[key] = (disc_scores[key] / max_score) * 10

    # Determinar perfil (ex: DI, SC, etc.)
    profile = generate_disc_profile(disc_scores)

    return DISCResult(
        d=disc_scores["D"],
        i=disc_scores["I"],
        s=disc_scores["S"],
        c=disc_scores["C"],
        profile=profile
    )

def generate_disc_profile(scores: dict) -> str:
    """
    Gera código DISC (ex: Di, SC, Dc)
    Maiúscula = score >= 7
    Minúscula = score >= 4
    """
    profile = ""
    for dimension in ["D", "I", "S", "C"]:
        score = scores[dimension]
        if score >= 7:
            profile += dimension
        elif score >= 4:
            profile += dimension.lower()

    return profile if profile else "balanced"
```

### 2. Espiral Dinâmica Scoring

```python
def calculate_spiral(responses: List[Response]) -> SpiralResult:
    """
    Calcula scores de Espiral Dinâmica.
    Usa sistema de dupla pontuação: algumas perguntas pontuam para múltiplas cores.
    """
    colors = {
        "beige": 0, "purple": 0, "red": 0, "blue": 0,
        "orange": 0, "green": 0, "yellow": 0, "turquoise": 0
    }

    for response in responses:
        question = response.question
        if "spiral" in question.metadata.get("frameworks", []):
            value = response.answer_value["value"]
            scoring = question.metadata["spiral_scoring"]

            for color, weight in scoring.items():
                colors[color] += value * weight

    # Normalizar
    total = sum(colors.values())
    for color in colors:
        colors[color] = (colors[color] / total) * 100

    # Identificar top 3 cores
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_colors[0][0]
    secondary = sorted_colors[1][0]
    tertiary = sorted_colors[2][0]

    # Gerar interpretações profundas usando knowledge base
    interpretations = generate_spiral_interpretations(
        primary, secondary, tertiary, colors
    )

    return SpiralResult(
        scores=colors,
        primary=primary,
        secondary=secondary,
        tertiary=tertiary,
        interpretations=interpretations
    )

def generate_spiral_interpretations(
    primary: str,
    secondary: str,
    tertiary: str,
    scores: dict
) -> dict:
    """
    Usa a knowledge base de Spiral Dynamics para gerar interpretações profundas.

    Exemplos de análises:
    - Roxo + Amarelo = "Pessoa evoluída cognitivamente mas presa por segurança/escassez"
    - Vermelho + Azul + Laranja = "Líder nato com estrutura e resultados"
    - Verde alto sozinho = "Risco de paralisia por consenso"
    """
    # Load knowledge base
    kb = load_spiral_knowledge_base()

    # Análise de combinações
    combination_key = f"{primary}+{secondary}"

    if combination_key in kb["combinations"]["problematic"]:
        # Combinação problemática detectada
        interpretation = kb["combinations"]["problematic"][combination_key]
        red_flags = True
    elif combination_key in kb["combinations"]["powerful"]:
        # Combinação poderosa
        interpretation = kb["combinations"]["powerful"][combination_key]
        red_flags = False
    else:
        # Combinação neutra, gerar baseado em descrições individuais
        interpretation = {
            "primary_description": kb["colors"][primary]["description"],
            "secondary_description": kb["colors"][secondary]["description"],
            "integration_notes": f"Integração de {primary} e {secondary}"
        }
        red_flags = False

    return {
        "combination": combination_key,
        "analysis": interpretation,
        "red_flags": red_flags,
        "development_path": kb["transitions"][primary]["next_stage"]
    }
```

### 3. PAEI Scoring

```python
def calculate_paei(responses: List[Response]) -> PAEIResult:
    """
    Calcula scores PAEI (Adizes).
    Usa dupla pontuação: perguntas DISC também pontuam para PAEI.
    """
    paei_scores = {"P": 0, "A": 0, "E": 0, "I": 0}

    for response in responses:
        question = response.question
        if "paei" in question.metadata.get("frameworks", []):
            value = response.answer_value["value"]
            scoring = question.metadata["paei_scoring"]

            for dimension, weight in scoring.items():
                paei_scores[dimension] += value * weight

    # Normalizar para 0-10
    max_score = max(paei_scores.values())
    for key in paei_scores:
        paei_scores[key] = (paei_scores[key] / max_score) * 10

    # Gerar código PAEI (ex: PaEi, PAeI)
    code = generate_paei_code(paei_scores)

    # Gerar interpretações
    interpretations = generate_paei_interpretations(code, paei_scores)

    return PAEIResult(
        p=paei_scores["P"],
        a=paei_scores["A"],
        e=paei_scores["E"],
        i=paei_scores["I"],
        code=code,
        interpretations=interpretations
    )

def generate_paei_code(scores: dict) -> str:
    """
    P/A/E/I maiúsculo = score >= 7
    p/a/e/i minúsculo = 4 <= score < 7
    - = score < 4
    """
    code = ""
    for dim in ["P", "A", "E", "I"]:
        score = scores[dim]
        if score >= 7:
            code += dim
        elif score >= 4:
            code += dim.lower()
        else:
            code += "-"
    return code

def generate_paei_interpretations(code: str, scores: dict) -> dict:
    """
    Interpretações baseadas no código PAEI.

    Exemplos:
    - paEi = "Visionário desorganizado - precisa urgente de COO"
    - Paei = "Workaholic solitário - burnout garantido"
    - PAeI = "Empresário equilibrado - manter e escalar"
    """
    patterns = {
        "paEi": {
            "title": "O Visionário Desorganizado",
            "strengths": ["Cheio de ideias", "Alta energia criativa"],
            "weaknesses": ["Caos administrativo", "Equipe perdida"],
            "critical_action": "Contratar COO com código PAeI urgente",
            "people_problems": "Equipe desmotivada por falta de estrutura",
            "financial_problems": "Fluxo de caixa caótico, sem controles"
        },
        "Paei": {
            "title": "O Workaholic Solitário",
            "strengths": ["Alta produção individual"],
            "weaknesses": ["Não delega", "Não inova", "Não sistematiza"],
            "critical_action": "Forçar delegação e contratar pessoas",
            "people_problems": "Não consegue formar equipe",
            "financial_problems": "Crescimento limitado pela capacidade individual"
        },
        # ... mais padrões
    }

    return patterns.get(code, generate_custom_interpretation(scores))
```

### 4. Eneagrama Scoring

```python
def calculate_enneagram(responses: List[Response]) -> EnneagramResult:
    """
    Calcula tipo de Eneagrama (1-9), asa (wing) e subtipo.
    """
    type_scores = {i: 0 for i in range(1, 10)}

    for response in responses:
        question = response.question
        if "enneagram" in question.metadata.get("frameworks", []):
            value = response.answer_value["value"]
            scoring = question.metadata["enneagram_scoring"]

            for type_num, weight in scoring.items():
                type_scores[int(type_num)] += value * weight

    # Tipo primário
    primary_type = max(type_scores, key=type_scores.get)

    # Wing (vizinho com score mais alto)
    neighbors = [primary_type - 1, primary_type + 1]
    neighbors = [n for n in neighbors if 1 <= n <= 9]
    wing = max(neighbors, key=lambda n: type_scores[n]) if neighbors else None

    # Subtipo (sp/so/sx) - determinado por perguntas específicas
    subtype = determine_subtype(responses)

    # Interpretações
    interpretations = generate_enneagram_interpretations(
        primary_type, wing, subtype
    )

    return EnneagramResult(
        type=primary_type,
        wing=f"{primary_type}w{wing}" if wing else str(primary_type),
        subtype=subtype,
        interpretations=interpretations
    )

def generate_enneagram_interpretations(
    type_num: int,
    wing: int,
    subtype: str
) -> dict:
    """
    Gera interpretações focadas em gestão de pessoas e finanças.

    Tipo 3 (Realizador):
    - Pessoas: Contrata "mini-mes", dificuldade com feedback honesto
    - Finanças: Gasta muito em imagem/marca

    Tipo 8 (Desafiador):
    - Pessoas: Conflitos agressivos, dificuldade de delegar (não confia)
    - Finanças: Decisões impulsivas de alto risco

    Tipo 9 (Pacificador):
    - Pessoas: Procrastina demissões por meses
    - Finanças: Evita decisões difíceis (cortes, cobranças)
    """
    type_data = ENNEAGRAM_DATABASE[type_num]

    return {
        "core_motivation": type_data["motivation"],
        "core_fear": type_data["fear"],
        "people_management": {
            "hiring_patterns": type_data["hiring_blind_spots"],
            "delegation_issues": type_data["delegation_problems"],
            "conflict_style": type_data["conflict_handling"],
            "team_impact": type_data["team_dynamics"]
        },
        "financial_patterns": {
            "spending_tendencies": type_data["financial_behavior"],
            "risk_profile": type_data["risk_approach"],
            "decision_making": type_data["financial_decisions"]
        },
        "growth_path": type_data["integration_direction"],
        "stress_behavior": type_data["disintegration_direction"]
    }
```

---

## API ENDPOINTS

### Authentication
```
POST   /api/v1/auth/register      - Criar nova conta
POST   /api/v1/auth/login         - Login e obter JWT
POST   /api/v1/auth/refresh       - Refresh token
GET    /api/v1/auth/me            - Dados do usuário logado
```

### Assessments
```
POST   /api/v1/assessments/start           - Iniciar novo assessment
GET    /api/v1/assessments/{id}            - Obter assessment específico
POST   /api/v1/assessments/{id}/complete   - Finalizar assessment
GET    /api/v1/assessments/my-assessments  - Listar assessments do usuário
```

### Questions
```
GET    /api/v1/questions                   - Listar perguntas (paginado)
GET    /api/v1/questions/{id}              - Obter pergunta específica
```

### Responses
```
POST   /api/v1/responses                   - Salvar resposta
GET    /api/v1/responses/{assessment_id}   - Listar respostas de um assessment
PATCH  /api/v1/responses/{id}              - Atualizar resposta
```

### Results
```
GET    /api/v1/results/{assessment_id}     - Obter resultados calculados
```

### Reports
```
POST   /api/v1/reports/generate            - Gerar relatório PDF
GET    /api/v1/reports/{id}                - Obter relatório específico
GET    /api/v1/reports/{id}/download       - Download PDF
```

### Admin
```
GET    /api/v1/admin/users                 - Listar todos usuários
GET    /api/v1/admin/assessments           - Listar todos assessments
GET    /api/v1/admin/dashboard             - Dashboard administrativo
POST   /api/v1/admin/users/{id}/activate   - Ativar/desativar usuário
```

---

## COMPONENTES FRONTEND

### Páginas Principais

1. **Landing Page** (`/`)
   - Hero section
   - Benefícios do assessment
   - Depoimentos
   - CTA para cadastro

2. **Cadastro** (`/register`)
   - Formulário de cadastro
   - Validações em tempo real
   - Feedback visual

3. **Login** (`/login`)
   - Formulário de login
   - Esqueci senha
   - Link para cadastro

4. **Questionário** (`/questionario`)
   - Perguntas paginadas (5-10 por página)
   - Barra de progresso
   - Navegação entre perguntas
   - Auto-save de respostas
   - Design limpo e focado

5. **Resultado** (`/resultado`)
   - Gráficos interativos
   - Resumo dos scores
   - Download de relatórios
   - Opção de agendar consultoria

6. **Dashboard Admin** (`/admin/dashboard`)
   - Estatísticas gerais
   - Usuários recentes
   - Assessments completados
   - Gráficos de conversão

7. **Gestão de Clientes** (`/admin/clientes`)
   - Lista de clientes
   - Filtros e busca
   - Visualizar resultados de cada cliente
   - Ações (ativar/desativar, etc.)

### Componentes de UI

- **QuestionCard**: Renderiza pergunta com tipo apropriado (Likert, múltipla escolha, etc.)
- **ProgressBar**: Mostra progresso do assessment
- **SpiralChart**: Gráfico radar colorido da Espiral Dinâmica
- **DISCChart**: Gráfico de barras DISC
- **PAEIChart**: Gráfico radar PAEI
- **EnneagramChart**: Diagrama do Eneagrama

---

## GERAÇÃO DE RELATÓRIOS

### Relatório Simplificado (2-3 páginas)

**Estrutura:**
1. **Capa**
   - Nome do usuário
   - Data do assessment
   - Logo "Jornada do Empreendedor de Sucesso"

2. **Resumo Executivo** (1 página)
   - Perfil DISC (ex: "DI - Líder Persuasivo")
   - Cores dominantes Espiral (ex: "Laranja-Verde")
   - Código PAEI (ex: "PaEi - Visionário Desorganizado")
   - Top 3 Valores Empresariais

3. **Gráficos** (1 página)
   - Gráfico DISC
   - Gráfico Espiral Dinâmica (colorido)
   - Gráfico PAEI

4. **Próximos Passos** (1 página)
   - 3 ações prioritárias
   - Recomendação de contratação básica
   - CTA para relatório completo + consultoria

### Relatório Completo (15-20 páginas)

**Estrutura:**

1. **Capa + Índice** (2 páginas)

2. **Introdução aos Frameworks** (1 página)
   - Breve explicação de cada metodologia

3. **Perfil DISC Detalhado** (2-3 páginas)
   - Gráfico DISC
   - Descrição do perfil (ex: DI)
   - Pontos fortes detalhados
   - Pontos fracos e blind spots
   - Como se comunica
   - Como toma decisões
   - Recomendações de desenvolvimento

4. **Análise Espiral Dinâmica Profunda** (3-4 páginas)
   - Gráfico Espiral colorido
   - Descrição das 3 cores dominantes
   - **Análise de Combinações** ⭐
     - "Roxo + Amarelo = conflito cognitivo..."
     - "Vermelho + Azul = empoderamento estruturado..."
   - Transições e próximo estágio evolutivo
   - Aplicações em negócios para cada cor
   - Red flags específicos

5. **Gestão e Liderança - PAEI** (2-3 páginas)
   - Gráfico PAEI
   - Interpretação do código (ex: "paEi")
   - **Problemas com Pessoas** ⭐
     - Padrões de contratação
     - Dificuldades de delegação
     - Estilo de comunicação com equipe
   - **Problemas Financeiros** ⭐
     - Tendências de gastos
     - Decisões financeiras
   - Recomendações de contratação específicas

6. **Autossabotagem - Eneagrama** (2-3 páginas)
   - Diagrama do Eneagrama
   - Tipo principal + asa + subtipo
   - Motivações profundas
   - Medos inconscientes
   - **Padrões de Autossabotagem** ⭐
     - Com pessoas
     - Com dinheiro
     - Sob stress
   - Caminhos de crescimento (integração)

7. **Valores e Cultura** (1-2 páginas)
   - Top 3 valores empresariais
   - Arquétipos de pessoas que busca contratar
   - Gaps entre perfil atual e perfil desejado

8. **Síntese Integrada** (2 páginas)
   - Como todos os frameworks se conectam
   - Padrões dominantes cruzados
   - Mensagem central do perfil

9. **Plano de Ação** (2-3 páginas)
   - 30 dias: Ações críticas
   - 60 dias: Ações importantes
   - 90 dias: Ações de médio prazo
   - Contratações recomendadas (específicas por perfil)
   - Recursos e ferramentas

10. **Anexos** (1 página)
    - Glossário de termos
    - Referências bibliográficas

---

## DESIGN SYSTEM

### Cores

**Espiral Dinâmica (fiéis ao original):**
- Bege: `#F5DEB3`
- Roxo: `#9370DB`
- Vermelho: `#DC143C`
- Azul: `#4169E1`
- Laranja: `#FF8C00`
- Verde: `#32CD32`
- Amarelo: `#FFD700`
- Turquesa: `#40E0D0`

**DISC:**
- D (Dominance): `#FF4444` (Vermelho)
- I (Influence): `#FFD700` (Amarelo/Ouro)
- S (Steadiness): `#4CAF50` (Verde)
- C (Conscientiousness): `#2196F3` (Azul)

**PAEI:**
- P (Producer): `#FF5722` (Laranja forte)
- A (Administrator): `#3F51B5` (Azul escuro)
- E (Entrepreneur): `#FFEB3B` (Amarelo)
- I (Integrator): `#4CAF50` (Verde)

**UI Geral:**
- Primary: `#6366F1` (Indigo)
- Secondary: `#8B5CF6` (Purple)
- Success: `#10B981` (Green)
- Warning: `#F59E0B` (Amber)
- Error: `#EF4444` (Red)
- Background: `#F9FAFB` (Gray 50)
- Text: `#111827` (Gray 900)

### Tipografia
- **Headings:** Inter (semibold/bold)
- **Body:** Inter (regular/medium)
- **Monospace:** JetBrains Mono

---

## SEGURANÇA

### Autenticação
- JWT com refresh tokens
- Tokens expiram em 15 minutos (access) e 7 dias (refresh)
- Senhas hash com bcrypt (rounds=12)

### Autorização
- RBAC (Role-Based Access Control)
- Roles: `user`, `admin`
- Middlewares de proteção em rotas

### Validação
- Input validation com Pydantic (backend) e Zod (frontend)
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (sanitização de inputs)
- CORS configurado adequadamente

### Rate Limiting
- Limite de requests por IP
- Proteção contra brute force em login

---

## PERFORMANCE

### Backend
- Conexões de DB com pooling
- Cache de resultados calculados (Redis opcional)
- Paginação em listagens
- Índices no banco de dados

### Frontend
- Code splitting automático (Next.js)
- Lazy loading de componentes
- Imagens otimizadas (next/image)
- Caching de API responses

---

## TESTES

### Backend
- Unit tests: Algoritmos de scoring
- Integration tests: Endpoints da API
- Coverage mínimo: 80%

### Frontend
- Component tests: UI components
- E2E tests: Fluxos principais (Playwright)
- Coverage mínimo: 70%

---

## DEPLOY

### Ambiente de Desenvolvimento
```bash
docker-compose up -d
```

### Ambiente de Produção

**Frontend (Vercel):**
- Deploy automático via GitHub
- Preview deployments em PRs
- Custom domain

**Backend (Railway/Render):**
- Deploy automático via GitHub
- PostgreSQL managed
- Environment variables
- Health checks

---

## PRÓXIMOS PASSOS DE DESENVOLVIMENTO

1. ✅ Setup inicial do projeto (estrutura de pastas)
2. ✅ Modelagem do banco de dados
3. ⏳ Implementação dos algoritmos de scoring
4. ⏳ Desenvolvimento da API (endpoints principais)
5. ⏳ Desenvolvimento do frontend (páginas principais)
6. ⏳ Integração dos componentes
7. ⏳ Geração de relatórios PDF
8. ⏳ Testes e ajustes
9. ⏳ Deploy em staging
10. ⏳ Testes finais com usuário
11. ⏳ Deploy em produção

---

**Versão:** 1.0.0
**Data:** 2026-03-12
**Autor:** Sistema AIOS
