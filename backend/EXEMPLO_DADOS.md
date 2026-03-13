# Exemplos de Dados nos Modelos

## 1. User (Exemplo Completo)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "joao.silva@example.com",
  "password_hash": "$2b$12$R9h7cIPz0gi.URNNGJVSA.92u5/RKLw4gblF.LqHSiZx5QkKjWPK",
  "full_name": "João Silva",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-03-10T14:30:00+00:00",
  "updated_at": "2024-03-10T14:30:00+00:00"
}
```

---

## 2. Assessment (Exemplo)

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "started_at": "2024-03-12T09:00:00+00:00",
  "completed_at": null,
  "current_question_index": 25,
  "total_questions": 105,
  "metadata": {
    "session_id": "sess_123456",
    "browser": "Chrome/120.0",
    "ip_address": "192.168.1.1",
    "language": "pt-BR",
    "device_type": "desktop"
  },
  "created_at": "2024-03-12T09:00:00+00:00",
  "updated_at": "2024-03-12T10:15:00+00:00"
}
```

---

## 3. Question (Exemplo Likert 5)

```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "question_text": "Prefiro trabalhar de forma independente e tomar minhas próprias decisões.",
  "question_type": "likert_5",
  "section": "comportamento_valores",
  "order_index": 1,
  "is_active": true,
  "metadata": {
    "options": [
      "Discordo totalmente",
      "Discordo",
      "Neutro",
      "Concordo",
      "Concordo totalmente"
    ],
    "scoring_rules": {
      "values": [1, 2, 3, 4, 5],
      "maps_to": {
        "disc_d": 0.8,
        "paei_e": 0.6
      }
    },
    "section_weight": 1.0
  },
  "created_at": "2024-03-01T00:00:00+00:00"
}
```

### Exemplo com Multiple Choice

```json
{
  "id": "880e8400-e29b-41d4-a716-446655440003",
  "question_text": "Em uma situação de pressão, qual é sua reação natural?",
  "question_type": "multiple_choice",
  "section": "comportamento_valores",
  "order_index": 2,
  "is_active": true,
  "metadata": {
    "options": [
      {
        "id": "opt_1",
        "text": "Agir rapidamente e assumir riscos",
        "value": 1
      },
      {
        "id": "opt_2",
        "text": "Analisar a situação cuidadosamente",
        "value": 2
      },
      {
        "id": "opt_3",
        "text": "Consultar os outros e buscar consensus",
        "value": 3
      }
    ],
    "scoring_rules": {
      "opt_1": {"disc_d": 1.0, "spiral_red": 0.8},
      "opt_2": {"disc_c": 1.0, "spiral_blue": 0.8},
      "opt_3": {"disc_i": 0.8, "spiral_green": 0.6}
    }
  },
  "created_at": "2024-03-01T00:00:00+00:00"
}
```

---

## 4. Response (Exemplo)

```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "assessment_id": "660e8400-e29b-41d4-a716-446655440001",
  "question_id": "770e8400-e29b-41d4-a716-446655440002",
  "answer_value": {
    "value": 5,
    "raw_value": "Concordo totalmente",
    "timestamp_ms": 3200
  },
  "answered_at": "2024-03-12T09:05:32+00:00"
}
```

### Exemplo com Multiple Choice

```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440005",
  "assessment_id": "660e8400-e29b-41d4-a716-446655440001",
  "question_id": "880e8400-e29b-41d4-a716-446655440003",
  "answer_value": {
    "option_id": "opt_1",
    "option_text": "Agir rapidamente e assumir riscos",
    "value": 1
  },
  "answered_at": "2024-03-12T09:06:15+00:00"
}
```

---

## 5. Result (Exemplo Completo)

```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440006",
  "assessment_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  
  "disc_d": 72.50,
  "disc_i": 58.30,
  "disc_s": 45.20,
  "disc_c": 39.80,
  "disc_profile": "DI",
  
  "spiral_beige": 5.00,
  "spiral_purple": 12.00,
  "spiral_red": 18.50,
  "spiral_blue": 22.30,
  "spiral_orange": 28.50,
  "spiral_green": 18.20,
  "spiral_yellow": 8.50,
  "spiral_turquoise": 2.00,
  "spiral_primary": "orange",
  "spiral_secondary": "blue",
  "spiral_tertiary": "red",
  
  "paei_p": 68.00,
  "paei_a": 52.00,
  "paei_e": 75.00,
  "paei_i": 48.00,
  "paei_code": "PaEi",
  
  "enneagram_type": 8,
  "enneagram_wing": "8w7",
  "enneagram_subtype": "social",
  
  "valores_primary": "Liderança",
  "valores_secondary": "Inovação",
  "valores_tertiary": "Resultado",
  
  "arquetipos": {
    "primary": "O Líder",
    "secondary": "O Empreendedor",
    "description": "Perfil de liderança forte e empreendedora"
  },
  
  "interpretations": {
    "disc_interpretation": "Você é uma pessoa dominante e influente, com tendência a tomar decisões rápidas e liderar com confiança.",
    "spiral_interpretation": "Seu desenvolvimento está centrado no nível Laranja (Moderno) com raízes em Azul (Tradicional). Você é orientado a resultados e a inovação.",
    "paei_interpretation": "Seu perfil é forte em Produtor e Empreendedor, o que indica excelente capacidade de execução e inovação."
  },
  
  "recommendations": {
    "leadership": "Desenvolva habilidades de escuta ativa para melhorar a inteligência emocional.",
    "development": "Considere explorar habilidades de administração para melhorar eficiência operacional.",
    "team_composition": "Trabalhe com pessoas que complementem seus pontos fracos em S (Estabilidade) e C (Conformidade).",
    "suggested_roles": ["CEO", "Empreendedor", "Diretor de Inovação", "Líder de Transformação"]
  },
  
  "created_at": "2024-03-12T11:00:00+00:00"
}
```

---

## 6. Report (Exemplo)

```json
{
  "id": "cc0e8400-e29b-41d4-a716-446655440007",
  "result_id": "bb0e8400-e29b-41d4-a716-446655440006",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "report_type": "complete",
  "pdf_path": "/reports/2024/03/joao_silva_550e8400_complete_20240312.pdf",
  "generated_at": "2024-03-12T11:15:00+00:00",
  "metadata": {
    "version": "1.0",
    "language": "pt-BR",
    "timezone": "America/Sao_Paulo",
    "file_size_kb": 2458,
    "pages": 15,
    "includes_recommendations": true,
    "includes_graphics": true,
    "generated_by": "report_service_v1.0"
  }
}
```

---

## Fluxo Completo de Dados

### Passo 1: Usuário se registra
```
POST /api/users
{
  "email": "joao.silva@example.com",
  "password": "senha_segura_aqui",
  "full_name": "João Silva"
}
→ Cria User
```

### Passo 2: Inicia uma avaliação
```
POST /api/assessments
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
→ Cria Assessment com status = "in_progress"
```

### Passo 3: Responde as 105 questões
```
POST /api/responses
{
  "assessment_id": "660e8400-e29b-41d4-a716-446655440001",
  "question_id": "770e8400-e29b-41d4-a716-446655440002",
  "answer_value": {"value": 5}
}
→ Cria Response (1x para cada questão = 105 responses)
```

### Passo 4: Completa a avaliação
```
PATCH /api/assessments/660e8400-e29b-41d4-a716-446655440001
{
  "status": "completed",
  "completed_at": "2024-03-12T11:00:00+00:00"
}
```

### Passo 5: Sistema calcula os resultados
```
POST /api/results/calculate
{
  "assessment_id": "660e8400-e29b-41d4-a716-446655440001"
}
→ Engine processa respostas e cria Result com todos os scores
```

### Passo 6: Gera relatório
```
POST /api/reports
{
  "result_id": "bb0e8400-e29b-41d4-a716-446655440006",
  "report_type": "complete"
}
→ Cria PDF e registra Report
```

### Passo 7: Usuário visualiza resultado
```
GET /api/results/550e8400-e29b-41d4-a716-446655440000
→ Retorna Result com todos os scores e interpretações
```

---

## Tamanhos Estimados de Dados

| Campo | Exemplo | Bytes |
|-------|---------|-------|
| UUID | 550e8400-e29b-41d4-a716-446655440000 | 36 |
| Email | joao.silva@example.com | 24 |
| Password Hash | $2b$12$R9h7cIPz0gi.URNNGJVSA... | 60 |
| Full Name | João Silva | 11 |
| DISC Score | 72.50 | 5 |
| JSON metadata | {...} | 500-1000 |

---

## Queries Comuns

### Obter todas as avaliações de um usuário
```sql
SELECT a.* FROM assessments a
WHERE a.user_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY a.created_at DESC;
```

### Obter respostas de uma avaliação
```sql
SELECT r.*, q.question_text FROM responses r
JOIN questions q ON r.question_id = q.id
WHERE r.assessment_id = '660e8400-e29b-41d4-a716-446655440001'
ORDER BY q.order_index;
```

### Buscar usuários com perfil DISC específico
```sql
SELECT u.*, r.* FROM users u
JOIN results r ON u.id = r.user_id
WHERE r.disc_profile = 'DI'
AND u.is_active = true;
```

### Usuários com mais de um relatório
```sql
SELECT u.email, COUNT(r.id) as report_count
FROM users u
JOIN reports r ON u.id = r.user_id
GROUP BY u.id
HAVING COUNT(r.id) > 1;
```

