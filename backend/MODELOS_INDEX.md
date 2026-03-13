# Índice Completo de Modelos SQLAlchemy

## Estrutura de Diretórios

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py              (18 linhas)
│   │   ├── user.py                  (38 linhas)
│   │   ├── assessment.py            (41 linhas)
│   │   ├── question.py              (37 linhas)
│   │   ├── response.py              (35 linhas)
│   │   ├── result.py                (84 linhas)
│   │   ├── report.py                (36 linhas)
│   │   └── README.md                (documentação visual)
│   ├── db/
│   │   ├── base.py                  (importa modelos)
│   │   └── session.py
│   └── ...
├── MODELOS.md                        (documentação completa)
├── EXEMPLO_DADOS.md                 (exemplos de dados)
├── QUICK_REFERENCE.md               (referência rápida)
└── ...
```

---

## 1. User Model

**Arquivo:** `/app/models/user.py`

Representa um usuário do sistema.

### Estrutura
```python
class User(Base):
    __tablename__ = "users"
    
    # Primary Key
    id: UUID                           # uuid.uuid4()
    
    # Core Fields
    email: str                         # VARCHAR(255) UNIQUE NOT NULL
    password_hash: str                 # VARCHAR(255) NOT NULL
    full_name: str                     # VARCHAR(255) NOT NULL
    is_active: bool = True            # BOOLEAN DEFAULT TRUE
    is_admin: bool = False            # BOOLEAN DEFAULT FALSE
    
    # Timestamps
    created_at: datetime              # DateTime(tz) DEFAULT now()
    updated_at: datetime              # DateTime(tz) DEFAULT now() ON UPDATE
    
    # Relationships
    assessments: List[Assessment]     # 1:N
    results: List[Result]             # 1:N
    reports: List[Report]             # 1:N
```

### Índices
- `email` (UNIQUE)
- `is_active`

### Casca de Deleção
```
User DELETE → Assessment (cascade) → Response (cascade)
           → Result (cascade) → Report (cascade)
           → Report (cascade)
```

---

## 2. Assessment Model

**Arquivo:** `/app/models/assessment.py`

Representa uma sessão de avaliação/questionário.

### Estrutura
```python
class Assessment(Base):
    __tablename__ = "assessments"
    
    # Primary Key
    id: UUID                          # uuid.uuid4()
    
    # Foreign Keys
    user_id: UUID                     # FK → users.id
    
    # Status
    status: str                       # VARCHAR(50) - in_progress|completed|abandoned
    
    # Timestamps
    started_at: datetime              # DateTime(tz)
    completed_at: datetime | None     # DateTime(tz) nullable
    
    # Progress
    current_question_index: int = 0   # 0-104
    total_questions: int = 105        # sempre 105
    
    # Metadata
    metadata: dict                    # JSON - session, browser, device info
    
    # System Timestamps
    created_at: datetime              # DateTime(tz)
    updated_at: datetime              # DateTime(tz)
    
    # Relationships
    user: User                        # N:1
    responses: List[Response]         # 1:N
    result: Result | None             # 1:1 optional
```

### Índices
- `user_id` (FK)
- `status`

### Status Values
- `"in_progress"` - Avaliação em andamento
- `"completed"` - Avaliação concluída
- `"abandoned"` - Avaliação abandonada

---

## 3. Question Model

**Arquivo:** `/app/models/question.py`

Representa uma questão do banco de questões.

### Estrutura
```python
class Question(Base):
    __tablename__ = "questions"
    
    # Primary Key
    id: UUID                          # uuid.uuid4()
    
    # Question Content
    question_text: str                # TEXT NOT NULL
    
    # Type and Section
    question_type: str                # VARCHAR(50) - likert_5|multiple_choice|ranking|text
    section: str                      # VARCHAR(100) - comportamento_valores, lideranca, etc
    
    # Ordering
    order_index: int                  # INTEGER - 1-105
    
    # Status
    is_active: bool = True            # BOOLEAN DEFAULT TRUE
    
    # Metadata
    metadata: dict                    # JSON - options, scoring_rules, weights
    
    # System
    created_at: datetime              # DateTime(tz)
    
    # Relationships
    responses: List[Response]         # 1:N
```

### Índices
- `question_type`
- `section`
- `order_index`
- `is_active`

### Question Types
- `"likert_5"` - Escala de Likert 5 pontos
- `"multiple_choice"` - Múltipla escolha
- `"ranking"` - Ranking
- `"text"` - Texto livre

---

## 4. Response Model

**Arquivo:** `/app/models/response.py`

Representa a resposta de um usuário para uma questão.

### Estrutura
```python
class Response(Base):
    __tablename__ = "responses"
    
    # Primary Key
    id: UUID                          # uuid.uuid4()
    
    # Foreign Keys
    assessment_id: UUID               # FK → assessments.id (CASCADE)
    question_id: UUID                 # FK → questions.id (RESTRICT)
    
    # Answer
    answer_value: dict                # JSON - flexible format
    
    # Timestamp
    answered_at: datetime             # DateTime(tz)
    
    # Relationships
    assessment: Assessment            # N:1
    question: Question                # N:1
```

### Índices
- `assessment_id` (FK)
- `question_id` (FK)

### Answer Value Formats

#### Likert 5
```json
{
  "value": 5,
  "raw_value": "Concordo totalmente",
  "timestamp_ms": 3200
}
```

#### Multiple Choice
```json
{
  "option_id": "opt_1",
  "option_text": "Agir rapidamente",
  "value": 1
}
```

#### Ranking
```json
{
  "ranking": [1, 3, 2, 4, 5],
  "items": ["Liderança", "Inovação", "Resultado", ...]
}
```

---

## 5. Result Model (PRINCIPAL)

**Arquivo:** `/app/models/result.py`

Contém todos os scores calculados da avaliação.

### Estrutura

#### Identifiers
```python
id: UUID                            # uuid.uuid4()
assessment_id: UUID                 # FK UNIQUE
user_id: UUID                       # FK
```

#### DISC Scores (0-100)
```python
disc_d: Decimal(5,2)               # Dominância
disc_i: Decimal(5,2)               # Influência
disc_s: Decimal(5,2)               # Estabilidade
disc_c: Decimal(5,2)               # Conformidade
disc_profile: str                  # "D", "DI", "DS", etc
```

#### Spiral Dynamics (0-100)
```python
spiral_beige: Decimal(5,2)        # Instinto
spiral_purple: Decimal(5,2)       # Tribal
spiral_red: Decimal(5,2)          # Impulsivo
spiral_blue: Decimal(5,2)         # Tradicional
spiral_orange: Decimal(5,2)       # Moderno
spiral_green: Decimal(5,2)        # Pós-moderno
spiral_yellow: Decimal(5,2)       # Integrador
spiral_turquoise: Decimal(5,2)    # Holístico

spiral_primary: str               # ex: "orange"
spiral_secondary: str | None      # ex: "blue"
spiral_tertiary: str | None       # ex: "red"
```

#### PAEI Scores (0-100)
```python
paei_p: Decimal(5,2)              # Produtor
paei_a: Decimal(5,2)              # Administrador
paei_e: Decimal(5,2)              # Empreendedor
paei_i: Decimal(5,2)              # Integrador
paei_code: str                    # "PAEI", "PaEi", etc
```

#### Enneagrama
```python
enneagram_type: int               # 1-9
enneagram_wing: str | None        # "8w7", "3w4"
enneagram_subtype: str | None     # "social", "sexual", "self-preservation"
```

#### Valores
```python
valores_primary: str              # "Liderança"
valores_secondary: str | None     # "Inovação"
valores_tertiary: str | None      # "Resultado"
```

#### JSON Fields
```python
arquetipos: dict                  # {"primary": "O Líder", ...}
interpretations: dict             # Texto das interpretações
recommendations: dict             # Recomendações personalizadas
```

#### System
```python
created_at: datetime              # DateTime(tz)
```

### Índices
- `assessment_id` (UNIQUE FK)
- `user_id` (FK)

### Valores Padrão para Spiral
```python
default=0  # Spiral scores iniciam em 0
```

---

## 6. Report Model

**Arquivo:** `/app/models/report.py`

Representa um relatório gerado.

### Estrutura
```python
class Report(Base):
    __tablename__ = "reports"
    
    # Primary Key
    id: UUID                          # uuid.uuid4()
    
    # Foreign Keys
    result_id: UUID                   # FK → results.id
    user_id: UUID                     # FK → users.id
    
    # Report Details
    report_type: str                  # VARCHAR(50) - simplified|complete
    pdf_path: str | None              # VARCHAR(500) - /reports/...pdf
    
    # Timestamp
    generated_at: datetime            # DateTime(tz) DEFAULT now()
    
    # Metadata
    metadata: dict                    # JSON - version, language, file_size, etc
    
    # Relationships
    result: Result                    # N:1
    user: User                        # N:1
```

### Índices
- `result_id` (FK)
- `user_id` (FK)
- `report_type`

### Report Types
- `"simplified"` - Relatório resumido (5-8 páginas)
- `"complete"` - Relatório completo (15-20 páginas)

### Metadata Example
```json
{
  "version": "1.0",
  "language": "pt-BR",
  "timezone": "America/Sao_Paulo",
  "file_size_kb": 2458,
  "pages": 15,
  "includes_recommendations": true,
  "includes_graphics": true,
  "generated_by": "report_service_v1.0"
}
```

---

## Relacionamentos (Entity-Relationship Diagram)

### Many-to-One
```
Assessment → User (N:1)
Response → Assessment (N:1)
Response → Question (N:1)
Result → User (N:1)
Result → Assessment (1:1)
Report → User (N:1)
Report → Result (N:1)
```

### One-to-Many (Reverse)
```
User ← Assessment (1:N)
Assessment ← Response (1:N)
Question ← Response (1:N)
User ← Result (1:N)
Assessment ← Result (1:1)
User ← Report (1:N)
Result ← Report (1:N)
```

---

## Fluxo de Dados Típico

```
1. REGISTRATION
   POST /api/users
   → Create User

2. START ASSESSMENT
   POST /api/assessments
   → Create Assessment (status: "in_progress")

3. ANSWER QUESTIONS
   POST /api/responses (x105)
   → Create Response for each question

4. COMPLETE ASSESSMENT
   PATCH /api/assessments/{id}
   → Update status to "completed"
   → Set completed_at timestamp

5. CALCULATE RESULTS
   POST /api/results/calculate
   → Engine processes all responses
   → Calculate all scores (DISC, Spiral, PAEI, Enneagram)
   → Create Result record

6. GENERATE REPORT
   POST /api/reports
   → Generate PDF
   → Create Report record

7. VIEW RESULTS
   GET /api/results/{user_id}
   → Return Result with all scores
   GET /api/reports/{user_id}
   → Return available reports
```

---

## Campos Totais por Tabela

| Tabela | Campos | PK | FK | Índices |
|--------|--------|----|----|---------|
| users | 8 | 1 | 0 | 2 |
| assessments | 10 | 1 | 1 | 2 |
| questions | 8 | 1 | 0 | 4 |
| responses | 5 | 1 | 2 | 2 |
| results | 39 | 1 | 2 | 2 |
| reports | 7 | 1 | 2 | 3 |
| **TOTAL** | **77** | **6** | **9** | **15** |

---

## Tipos de Dados Utilizados

| Tipo | Uso | Exemplos |
|------|-----|----------|
| UUID | Primary & Foreign Keys | id, user_id, assessment_id |
| VARCHAR(255) | Texto curto | email, password_hash, full_name |
| VARCHAR(50) | Status/Tipos | status, question_type, report_type |
| VARCHAR(100) | Categorias | section, valores_primary |
| TEXT | Texto longo | question_text |
| BOOLEAN | Flags | is_active, is_admin |
| INTEGER | Contadores | order_index, enneagram_type |
| NUMERIC(5,2) | Scores | disc_d, spiral_orange (0-99.99) |
| DateTime(tz) | Timestamps | created_at, answered_at |
| JSON | Dados flexíveis | metadata, answer_value |

---

## Validações no Schema

### User
- Email: Único, formato válido (validar no Pydantic)
- password_hash: Não pode ser vazio, usar bcrypt/argon2
- full_name: Não pode ser vazio

### Assessment
- status: Apenas in_progress, completed, abandoned
- current_question_index: 0 ≤ index ≤ 104
- total_questions: Sempre 105
- completed_at ≥ started_at

### Question
- question_type: Apenas likert_5, multiple_choice, ranking, text
- order_index: Deve ser único por seção
- metadata: Deve conter opções e regras

### Response
- answer_value: Deve corresponder ao question_type
- answered_at ≥ assessment.started_at

### Result
- Exatamente 1 por assessment
- DISC: 0-100, soma ~100
- PAEI: 0-100, soma ~100
- Spiral: 0-100
- enneagram_type: 1-9

### Report
- report_type: simplified ou complete
- Apenas 1 por result
- pdf_path: Preenchido quando gerado

---

## Imports Necessários

```python
# Models
from app.models import User, Assessment, Question, Response, Result, Report

# Database
from app.db.base import Base
from sqlalchemy.orm import Session

# Types
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

# Utilities
import uuid
from datetime import datetime
from decimal import Decimal
```

---

## Próximas Etapas

1. **Migrations** - `alembic revision --autogenerate`
2. **Schemas** - Criar Pydantic schemas para validação
3. **Services** - Implementar lógica de negócio
4. **API** - Endpoints FastAPI
5. **Tests** - Testes unitários
6. **Engine** - Scoring engine
7. **Reports** - Template de relatórios

---

## Referências de Arquivo

- **User Model**: `/app/models/user.py`
- **Assessment Model**: `/app/models/assessment.py`
- **Question Model**: `/app/models/question.py`
- **Response Model**: `/app/models/response.py`
- **Result Model**: `/app/models/result.py`
- **Report Model**: `/app/models/report.py`
- **Package Init**: `/app/models/__init__.py`
- **Base Config**: `/app/db/base.py` (imports all models)

---

**Data de Criação:** 12/03/2024  
**Status:** Completo e Validado
**Total de Linhas:** 289 linhas Python + documentação

