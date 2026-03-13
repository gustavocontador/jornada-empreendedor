# Modelos SQLAlchemy - Jornada do Empreendedor de Sucesso

## Visão Geral

Sistema completo de modelos ORM para a plataforma de avaliação comportamental e de liderança. Total de 6 tabelas com relacionamentos bidireccionais e indices otimizados.

---

## 1. User (Usuário)

**Arquivo:** `app/models/user.py`

Representa um usuário do sistema que pode realizar avaliações.

### Campos:
- `id` (UUID PK): Identificador único
- `email` (VARCHAR 255, UNIQUE, NOT NULL): Email único do usuário
- `password_hash` (VARCHAR 255, NOT NULL): Hash da senha
- `full_name` (VARCHAR 255, NOT NULL): Nome completo
- `is_active` (BOOLEAN, DEFAULT TRUE): Usuário ativo/inativo
- `is_admin` (BOOLEAN, DEFAULT FALSE): Permissões de administrador
- `created_at` (DATETIME+TZ): Criação do usuário
- `updated_at` (DATETIME+TZ): Última atualização

### Índices:
- `email` (UNIQUE)
- `is_active`

### Relationships:
- **assessments** (1:N) → Assessment
- **results** (1:N) → Result
- **reports** (1:N) → Report

---

## 2. Assessment (Avaliação)

**Arquivo:** `app/models/assessment.py`

Representa uma sessão de preenchimento do questionário completo (105 questões).

### Campos:
- `id` (UUID PK): Identificador único
- `user_id` (UUID FK): Referência ao usuário
- `status` (VARCHAR 50): Status da avaliação (in_progress, completed, abandoned)
- `started_at` (DATETIME+TZ): Início da avaliação
- `completed_at` (DATETIME+TZ): Conclusão da avaliação
- `current_question_index` (INTEGER): Índice da questão atual (0-104)
- `total_questions` (INTEGER, DEFAULT 105): Total de questões
- `metadata` (JSON): Dados adicionais (contexto, informações de sessão)
- `created_at` (DATETIME+TZ): Criação do registro
- `updated_at` (DATETIME+TZ): Última atualização

### Índices:
- `user_id` (FK)
- `status`

### Relationships:
- **user** (N:1) ← User
- **responses** (1:N) → Response
- **result** (1:1) → Result (opcional)

---

## 3. Question (Questão)

**Arquivo:** `app/models/question.py`

Representa uma pergunta individual do questionário.

### Campos:
- `id` (UUID PK): Identificador único
- `question_text` (TEXT, NOT NULL): Texto da questão
- `question_type` (VARCHAR 50): Tipo (likert_5, multiple_choice, ranking, text)
- `section` (VARCHAR 100): Seção (intro, comportamento_valores, lideranca, etc)
- `order_index` (INTEGER): Ordem de apresentação (1-105)
- `is_active` (BOOLEAN, DEFAULT TRUE): Questão ativa/inativa
- `metadata` (JSON): Opções de resposta, regras de pontuação, pesos
- `created_at` (DATETIME+TZ): Criação da questão

### Índices:
- `question_type`
- `section`
- `order_index`
- `is_active`

### Relationships:
- **responses** (1:N) → Response

---

## 4. Response (Resposta)

**Arquivo:** `app/models/response.py`

Representa a resposta de um usuário para uma questão específica.

### Campos:
- `id` (UUID PK): Identificador único
- `assessment_id` (UUID FK): Referência à avaliação
- `question_id` (UUID FK): Referência à questão
- `answer_value` (JSON): Valor da resposta (suporta número, string, array, objeto)
- `answered_at` (DATETIME+TZ): Timestamp da resposta

### Índices:
- `assessment_id` (FK)
- `question_id` (FK)

### Relationships:
- **assessment** (N:1) ← Assessment
- **question** (N:1) ← Question

---

## 5. Result (Resultado)

**Arquivo:** `app/models/result.py`

Contém todos os scores calculados a partir das respostas.

### Campos DISC (0-100):
- `disc_d` (NUMERIC 5,2): Dominância
- `disc_i` (NUMERIC 5,2): Influência
- `disc_s` (NUMERIC 5,2): Estabilidade
- `disc_c` (NUMERIC 5,2): Conformidade
- `disc_profile` (VARCHAR 10): Perfil DISC (ex: "DIS", "CS")

### Campos Spiral Dynamics (0-100):
- `spiral_beige` (NUMERIC 5,2): Instinto
- `spiral_purple` (NUMERIC 5,2): Tribal
- `spiral_red` (NUMERIC 5,2): Impulsivo
- `spiral_blue` (NUMERIC 5,2): Tradicional
- `spiral_orange` (NUMERIC 5,2): Moderno
- `spiral_green` (NUMERIC 5,2): Pós-moderno
- `spiral_yellow` (NUMERIC 5,2): Integrador
- `spiral_turquoise` (NUMERIC 5,2): Holístico
- `spiral_primary` (VARCHAR 50): Nível primário
- `spiral_secondary` (VARCHAR 50): Nível secundário (opcional)
- `spiral_tertiary` (VARCHAR 50): Nível terciário (opcional)

### Campos PAEI (0-100):
- `paei_p` (NUMERIC 5,2): Produtor
- `paei_a` (NUMERIC 5,2): Administrador
- `paei_e` (NUMERIC 5,2): Empreendedor
- `paei_i` (NUMERIC 5,2): Integrador
- `paei_code` (VARCHAR 10): Código PAEI (ex: "PAEI", "paEi")

### Campos Enneagrama:
- `enneagram_type` (INTEGER): Tipo 1-9
- `enneagram_wing` (VARCHAR 10): Asa (ex: "8w9", "3w4")
- `enneagram_subtype` (VARCHAR 50): Subtipo (social, sexual, self-preservation)

### Campos Valores:
- `valores_primary` (VARCHAR 100): Valor principal
- `valores_secondary` (VARCHAR 100): Valor secundário (opcional)
- `valores_tertiary` (VARCHAR 100): Valor terciário (opcional)

### Campos Adicionais:
- `id` (UUID PK): Identificador único
- `assessment_id` (UUID FK UNIQUE): Referência à avaliação
- `user_id` (UUID FK): Referência ao usuário
- `arquetipos` (JSON): Arquetipos de liderança
- `interpretations` (JSON): Interpretações dos resultados
- `recommendations` (JSON): Recomendações personalizadas
- `created_at` (DATETIME+TZ): Criação do resultado

### Índices:
- `assessment_id` (UNIQUE FK)
- `user_id` (FK)

### Relationships:
- **assessment** (1:1) ← Assessment
- **user** (N:1) ← User
- **reports** (1:N) → Report

---

## 6. Report (Relatório)

**Arquivo:** `app/models/report.py`

Representa um relatório gerado a partir dos resultados da avaliação.

### Campos:
- `id` (UUID PK): Identificador único
- `result_id` (UUID FK): Referência ao resultado
- `user_id` (UUID FK): Referência ao usuário
- `report_type` (VARCHAR 50): Tipo (simplified, complete)
- `pdf_path` (VARCHAR 500): Caminho do arquivo PDF gerado
- `generated_at` (DATETIME+TZ): Data de geração
- `metadata` (JSON): Informações adicionais (versão, idioma, tamanho do arquivo, etc)

### Índices:
- `result_id` (FK)
- `user_id` (FK)
- `report_type`

### Relationships:
- **result** (N:1) ← Result
- **user** (N:1) ← User

---

## Diagrama de Relacionamentos

```
User (1) ──→ (*) Assessment
             ↓
           Response (*)
             ↑
           Question (1)

User (1) ──→ (*) Result
             ↓
           Report (*)

Assessment (1) ──→ (1) Result
```

---

## Índices Criados

| Tabela | Campo | Tipo | Razão |
|--------|-------|------|-------|
| users | email | UNIQUE | Garantir emails únicos |
| users | is_active | INDEX | Filtrar usuários ativos |
| assessments | user_id | FK INDEX | Buscar avaliações por usuário |
| assessments | status | INDEX | Filtrar por status |
| questions | question_type | INDEX | Filtrar por tipo |
| questions | section | INDEX | Filtrar por seção |
| questions | order_index | INDEX | Ordem de apresentação |
| questions | is_active | INDEX | Questões ativas |
| responses | assessment_id | FK INDEX | Respostas por avaliação |
| responses | question_id | FK INDEX | Respostas por questão |
| results | assessment_id | UNIQUE FK | Apenas um resultado por avaliação |
| results | user_id | FK INDEX | Resultados por usuário |
| reports | result_id | FK INDEX | Relatórios por resultado |
| reports | user_id | FK INDEX | Relatórios por usuário |
| reports | report_type | INDEX | Filtrar por tipo |

---

## Timestamps com Timezone

Todos os campos DateTime usam `DateTime(timezone=True)` para garantir:
- Armazenamento em UTC no banco de dados
- Compatibilidade com diferentes fusos horários
- Rastreabilidade precisa de eventos

---

## Cascata de Deleção

- **User DELETE** → Deleta em cascata: Assessments, Results, Reports
- **Assessment DELETE** → Deleta em cascata: Responses, Result
- **Result DELETE** → Deleta em cascata: Reports
- **Question DELETE** → RESTRICT (não pode ser deletada se houver Responses)

---

## Exemplo de Uso

```python
from app.models import User, Assessment, Result
from sqlalchemy.orm import Session

# Criar usuário
user = User(
    email="usuario@example.com",
    password_hash="hash_aqui",
    full_name="João Silva"
)

# Criar avaliação
assessment = Assessment(
    user_id=user.id,
    status="in_progress"
)

# Acessar relacionamentos
for response in assessment.responses:
    question = response.question
    print(f"Questão {question.order_index}: {response.answer_value}")

# Resultado com todos os scores
result = assessment.result
print(f"DISC: {result.disc_profile} (D:{result.disc_d}, I:{result.disc_i}, S:{result.disc_s}, C:{result.disc_c})")
print(f"Spiral Primary: {result.spiral_primary}")
print(f"PAEI Code: {result.paei_code}")
```

---

## Próximos Passos

1. Criar migrations com Alembic
2. Implementar Pydantic schemas para validação
3. Criar service layers para lógica de negócio
4. Implementar endpoints da API FastAPI
5. Adicionar testes unitários
