# SQLAlchemy Models - Jornada do Empreendedor de Sucesso

## Estrutura de Modelos

### 1. User Model
```python
# Localização: app/models/user.py

User
├── id: UUID (PK)
├── email: VARCHAR(255) [UNIQUE]
├── password_hash: VARCHAR(255)
├── full_name: VARCHAR(255)
├── is_active: BOOLEAN [DEFAULT: True]
├── is_admin: BOOLEAN [DEFAULT: False]
├── created_at: DateTime(tz)
├── updated_at: DateTime(tz)
└── Relationships:
    ├── assessments: [Assessment]
    ├── results: [Result]
    └── reports: [Report]
```

### 2. Assessment Model
```python
# Localização: app/models/assessment.py

Assessment
├── id: UUID (PK)
├── user_id: UUID (FK → users)
├── status: VARCHAR(50) [in_progress|completed|abandoned]
├── started_at: DateTime(tz)
├── completed_at: DateTime(tz) [nullable]
├── current_question_index: INTEGER
├── total_questions: INTEGER [DEFAULT: 105]
├── metadata: JSON
├── created_at: DateTime(tz)
├── updated_at: DateTime(tz)
└── Relationships:
    ├── user: User
    ├── responses: [Response]
    └── result: Result [optional]
```

### 3. Question Model
```python
# Localização: app/models/question.py

Question
├── id: UUID (PK)
├── question_text: TEXT
├── question_type: VARCHAR(50) [likert_5|multiple_choice|ranking|text]
├── section: VARCHAR(100)
├── order_index: INTEGER
├── is_active: BOOLEAN [DEFAULT: True]
├── metadata: JSON [options, scoring_rules]
├── created_at: DateTime(tz)
└── Relationships:
    └── responses: [Response]
```

### 4. Response Model
```python
# Localização: app/models/response.py

Response
├── id: UUID (PK)
├── assessment_id: UUID (FK → assessments)
├── question_id: UUID (FK → questions)
├── answer_value: JSON
├── answered_at: DateTime(tz)
└── Relationships:
    ├── assessment: Assessment
    └── question: Question
```

### 5. Result Model (Complexo - Todos os Scores)
```python
# Localização: app/models/result.py

Result
├── id: UUID (PK)
├── assessment_id: UUID (FK → assessments) [UNIQUE]
├── user_id: UUID (FK → users)
│
├── DISC Scores (0-100):
│   ├── disc_d: NUMERIC(5,2)
│   ├── disc_i: NUMERIC(5,2)
│   ├── disc_s: NUMERIC(5,2)
│   ├── disc_c: NUMERIC(5,2)
│   └── disc_profile: VARCHAR(10)
│
├── Spiral Dynamics (0-100):
│   ├── spiral_beige: NUMERIC(5,2)
│   ├── spiral_purple: NUMERIC(5,2)
│   ├── spiral_red: NUMERIC(5,2)
│   ├── spiral_blue: NUMERIC(5,2)
│   ├── spiral_orange: NUMERIC(5,2)
│   ├── spiral_green: NUMERIC(5,2)
│   ├── spiral_yellow: NUMERIC(5,2)
│   ├── spiral_turquoise: NUMERIC(5,2)
│   ├── spiral_primary: VARCHAR(50)
│   ├── spiral_secondary: VARCHAR(50) [nullable]
│   └── spiral_tertiary: VARCHAR(50) [nullable]
│
├── PAEI Scores (0-100):
│   ├── paei_p: NUMERIC(5,2)
│   ├── paei_a: NUMERIC(5,2)
│   ├── paei_e: NUMERIC(5,2)
│   ├── paei_i: NUMERIC(5,2)
│   └── paei_code: VARCHAR(10)
│
├── Enneagrama:
│   ├── enneagram_type: INTEGER (1-9)
│   ├── enneagram_wing: VARCHAR(10) [nullable]
│   └── enneagram_subtype: VARCHAR(50) [nullable]
│
├── Valores:
│   ├── valores_primary: VARCHAR(100)
│   ├── valores_secondary: VARCHAR(100) [nullable]
│   └── valores_tertiary: VARCHAR(100) [nullable]
│
├── JSON Fields:
│   ├── arquetipos: JSON
│   ├── interpretations: JSON
│   └── recommendations: JSON
│
├── created_at: DateTime(tz)
└── Relationships:
    ├── assessment: Assessment
    ├── user: User
    └── reports: [Report]
```

### 6. Report Model
```python
# Localização: app/models/report.py

Report
├── id: UUID (PK)
├── result_id: UUID (FK → results)
├── user_id: UUID (FK → users)
├── report_type: VARCHAR(50) [simplified|complete]
├── pdf_path: VARCHAR(500) [nullable]
├── generated_at: DateTime(tz)
├── metadata: JSON
└── Relationships:
    ├── result: Result
    └── user: User
```

---

## Database Schema Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        USERS                                  │
├──────────────────────────────────────────────────────────────┤
│ PK: id (UUID)                                                 │
│ UNIQUE: email                                                 │
│ password_hash, full_name, is_active, is_admin                │
│ created_at, updated_at                                        │
└──────────────────────────────────────────────────────────────┘
              ↓                          ↓                 ↓
       (1:N)  │                    (1:N) │            (1:N) │
              ↓                          ↓                 ↓
     ┌─────────────────────┐   ┌──────────────────┐  ┌──────────────────┐
     │  ASSESSMENTS        │   │    RESULTS       │  │    REPORTS       │
     ├─────────────────────┤   ├──────────────────┤  ├──────────────────┤
     │ PK: id (UUID)       │   │ PK: id (UUID)    │  │ PK: id (UUID)    │
     │ FK: user_id         │   │ FK: user_id (*)  │  │ FK: user_id (*)  │
     │ status              │   │ FK: assessment   │  │ FK: result_id    │
     │ current_question..  │   │ DISC scores (4)  │  │ report_type      │
     │ total_questions     │   │ Spiral (8+3)     │  │ pdf_path         │
     │ metadata            │   │ PAEI scores (4)  │  │ generated_at     │
     │ started_at          │   │ Enneagram (3)    │  │ metadata         │
     │ completed_at        │   │ Valores (3)      │  └──────────────────┘
     │ created_at          │   │ JSON fields (3)  │
     │ updated_at          │   │ created_at       │
     └─────────────────────┘   └──────────────────┘
              ↓
         (1:N) │
              ↓
     ┌─────────────────────┐
     │   RESPONSES         │
     ├─────────────────────┤
     │ PK: id (UUID)       │
     │ FK: assessment_id   │
     │ FK: question_id     │
     │ answer_value (JSON) │
     │ answered_at         │
     └─────────────────────┘
              ↑
         (N:1) │
              └─────────── QUESTIONS
                    ├─ PK: id (UUID)
                    ├─ question_text
                    ├─ question_type
                    ├─ section
                    ├─ order_index
                    ├─ is_active
                    ├─ metadata
                    └─ created_at
```

---

## Índices e Performance

### Primary Keys (UUID)
- Todos os modelos usam UUID como chave primária
- Gerado automaticamente com `uuid.uuid4()`
- Benefício: Distribuição distribuída, segurança

### Foreign Keys com Índices
- `assessments.user_id`
- `assessments.status`
- `questions.question_type`
- `questions.section`
- `questions.order_index`
- `responses.assessment_id`
- `responses.question_id`
- `results.assessment_id` (UNIQUE)
- `results.user_id`
- `reports.result_id`
- `reports.user_id`
- `users.email` (UNIQUE)
- `users.is_active`

---

## Validações Importantes

### User
- Email deve ser único
- Email deve ser válido (validação no schema)
- Password must be hashed (usar bcrypt/argon2)
- full_name não pode ser vazio

### Assessment
- Status deve ser: in_progress, completed, abandoned
- current_question_index: 0-104
- total_questions: sempre 105 (padrão)
- completed_at deve ser posterior a started_at

### Question
- question_type deve ser um dos valores pré-definidos
- order_index deve ser único por seção
- metadata deve conter opções e regras de pontuação

### Response
- answer_value deve estar no formato correto para o question_type
- answered_at deve ser posterior a assessment.started_at

### Result
- Exatamente um resultado por assessment
- DISC scores devem somar ~100%
- Scores PAEI devem somar ~100%
- Spiral primary deve ser um dos 8 níveis
- Enneagram type deve estar entre 1-9

### Report
- report_type deve ser: simplified ou complete
- Apenas um resultado por relatório
- pdf_path deve ser preenchido quando gerado

---

## Padrões Utilizados

### Timestamps
```python
created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### Cascade Rules
```python
# User deletion cascades to all related records
assessments = relationship("Assessment", cascade="all, delete-orphan")
results = relationship("Result", cascade="all, delete-orphan")
reports = relationship("Report", cascade="all, delete-orphan")
```

### JSON Fields
```python
metadata = Column(JSON, default=dict, nullable=False)  # For flexible data
```

---

## Migrations (Próximas Etapas)

```bash
# Criar migration automática
alembic revision --autogenerate -m "Initial models creation"

# Aplicar migration
alembic upgrade head
```

---

## Usage Example

```python
from sqlalchemy.orm import Session
from app.models import User, Assessment, Question, Response, Result, Report

# Create user
user = User(
    email="john@example.com",
    password_hash="hashed_password",
    full_name="John Doe"
)
db.add(user)
db.commit()

# Create assessment
assessment = Assessment(
    user_id=user.id,
    status="in_progress"
)
db.add(assessment)
db.commit()

# Get responses for assessment
responses = db.query(Response).filter_by(assessment_id=assessment.id).all()

# Create result after completion
result = Result(
    assessment_id=assessment.id,
    user_id=user.id,
    disc_d=65.0,
    disc_i=45.0,
    disc_s=55.0,
    disc_c=40.0,
    disc_profile="DI",
    paei_p=70.0,
    paei_a=60.0,
    paei_e=75.0,
    paei_i=50.0,
    paei_code="PAEI",
    enneagram_type=3,
    spiral_primary="orange"
)
db.add(result)
db.commit()

# Generate report
report = Report(
    result_id=result.id,
    user_id=user.id,
    report_type="complete",
    pdf_path="/reports/user_123_complete.pdf"
)
db.add(report)
db.commit()
```

---

## Files Created

1. `/app/models/user.py` - User model
2. `/app/models/assessment.py` - Assessment model
3. `/app/models/question.py` - Question model
4. `/app/models/response.py` - Response model
5. `/app/models/result.py` - Result model
6. `/app/models/report.py` - Report model
7. `/app/models/__init__.py` - Package initialization

---

## Próximos Passos

1. **Alembic Migrations** - Criar migrations automáticas
2. **Pydantic Schemas** - Criar schemas para validação
3. **Service Layer** - Implementar lógica de negócio
4. **API Endpoints** - Implementar rotas FastAPI
5. **Tests** - Testes unitários e de integração
