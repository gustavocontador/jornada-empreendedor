# Quick Reference - SQLAlchemy Models

## 1. Importing Models

```python
from app.models import User, Assessment, Question, Response, Result, Report
from app.db.base import Base
from sqlalchemy.orm import Session
```

## 2. User Model

```python
# Create
user = User(
    email="user@example.com",
    password_hash="hashed_pwd",
    full_name="John Doe",
    is_active=True,
    is_admin=False
)

# Query
user = session.query(User).filter(User.email == "user@example.com").first()
user = session.query(User).filter(User.is_active == True).all()

# Access relationships
assessments = user.assessments
results = user.results
reports = user.reports
```

## 3. Assessment Model

```python
# Create
assessment = Assessment(
    user_id=user_id,
    status="in_progress",  # or "completed", "abandoned"
    metadata={
        "session_id": "sess_123",
        "device_type": "desktop"
    }
)

# Query
assessments = session.query(Assessment).filter(
    Assessment.user_id == user_id,
    Assessment.status == "in_progress"
).all()

# Access relationships
user = assessment.user
responses = assessment.responses
result = assessment.result
```

## 4. Question Model

```python
# Query active questions
questions = session.query(Question).filter(
    Question.is_active == True
).order_by(Question.order_index).all()

# Get question by index
q = session.query(Question).filter(
    Question.section == "comportamento_valores",
    Question.order_index == 1
).first()

# Access metadata
options = q.metadata.get("options")
scoring_rules = q.metadata.get("scoring_rules")
```

## 5. Response Model

```python
# Create
response = Response(
    assessment_id=assessment_id,
    question_id=question_id,
    answer_value={"value": 5}  # JSON flexible
)

# Query
responses = session.query(Response).filter(
    Response.assessment_id == assessment_id
).order_by(Response.answered_at).all()

# Get with joined question
from sqlalchemy.orm import joinedload
responses = session.query(Response).filter(
    Response.assessment_id == assessment_id
).options(joinedload(Response.question)).all()

for resp in responses:
    print(f"Q{resp.question.order_index}: {resp.answer_value}")
```

## 6. Result Model (Main)

```python
# Create after all responses collected
result = Result(
    assessment_id=assessment_id,
    user_id=user_id,
    
    # DISC
    disc_d=72.50,
    disc_i=58.30,
    disc_s=45.20,
    disc_c=39.80,
    disc_profile="DI",
    
    # Spiral
    spiral_beige=5.0,
    spiral_purple=12.0,
    spiral_red=18.5,
    spiral_blue=22.3,
    spiral_orange=28.5,
    spiral_green=18.2,
    spiral_yellow=8.5,
    spiral_turquoise=2.0,
    spiral_primary="orange",
    spiral_secondary="blue",
    spiral_tertiary="red",
    
    # PAEI
    paei_p=68.0,
    paei_a=52.0,
    paei_e=75.0,
    paei_i=48.0,
    paei_code="PaEi",
    
    # Enneagram
    enneagram_type=8,
    enneagram_wing="8w7",
    enneagram_subtype="social",
    
    # Values
    valores_primary="Liderança",
    valores_secondary="Inovação",
    valores_tertiary="Resultado",
    
    # JSON
    arquetipos={"primary": "O Líder"},
    interpretations={...},
    recommendations={...}
)

# Query
result = session.query(Result).filter(
    Result.user_id == user_id
).order_by(Result.created_at.desc()).first()

# Filter by DISC profile
results = session.query(Result).filter(
    Result.disc_profile.in_(["D", "DI", "DS"])
).all()

# Filter by Spiral primary
results = session.query(Result).filter(
    Result.spiral_primary == "orange"
).all()
```

## 7. Report Model

```python
# Create
report = Report(
    result_id=result_id,
    user_id=user_id,
    report_type="complete",  # or "simplified"
    pdf_path="/reports/user_123_complete.pdf",
    metadata={
        "version": "1.0",
        "language": "pt-BR",
        "pages": 15
    }
)

# Query
reports = session.query(Report).filter(
    Report.user_id == user_id,
    Report.report_type == "complete"
).all()

# Check if PDF generated
if report.pdf_path:
    print(f"PDF available: {report.pdf_path}")
```

## 8. Common Queries

### Get user with all assessments and results
```python
user = session.query(User).filter(User.id == user_id).first()
print(f"User: {user.full_name}")
print(f"Assessments: {len(user.assessments)}")
print(f"Results: {len(user.results)}")
```

### Get completed assessment with all responses
```python
assessment = session.query(Assessment).filter(
    Assessment.id == assessment_id,
    Assessment.status == "completed"
).first()

responses = session.query(Response).filter(
    Response.assessment_id == assessment.id
).order_by(Response.question.order_index).all()

for resp in responses:
    q = resp.question
    print(f"[{q.order_index}] {q.question_text}")
    print(f"Answer: {resp.answer_value}")
    print()
```

### Get all DISC profiles distribution
```python
from sqlalchemy import func

distribution = session.query(
    Result.disc_profile,
    func.count(Result.id).label('count')
).group_by(Result.disc_profile).all()

for profile, count in distribution:
    print(f"{profile}: {count} users")
```

### Get users by spiral development level
```python
users_orange = session.query(User).join(Result).filter(
    Result.spiral_primary == "orange"
).all()
```

### Get assessment progress for user
```python
assessment = session.query(Assessment).filter(
    Assessment.id == assessment_id
).first()

progress = (assessment.current_question_index / assessment.total_questions) * 100
print(f"Progress: {progress:.1f}% ({assessment.current_question_index}/{assessment.total_questions})")
```

## 9. Transactions and Commits

```python
# Add and commit
try:
    session.add(user)
    session.commit()
except Exception as e:
    session.rollback()
    raise

# Add multiple
users = [User(...), User(...), User(...)]
session.add_all(users)
session.commit()

# Update
user.full_name = "New Name"
session.commit()

# Delete (with cascade rules)
session.delete(user)  # Deletes assessments, results, reports automatically
session.commit()
```

## 10. Relationship Access

```python
# One-to-Many (lazy loading)
assessment.responses  # Returns all Response objects

# Many-to-One
response.assessment  # Returns single Assessment object
response.question    # Returns single Question object

# Back references
user.assessments  # Same as session.query(Assessment).filter(...user...)
result.reports    # Same as session.query(Report).filter(...result...)
```

## 11. DateTime Handling

```python
from datetime import datetime

# Create with automatic timestamp
assessment = Assessment(user_id=user_id)  # created_at set automatically

# All timestamps are in UTC
assessment.created_at  # datetime(2024, 3, 12, 10, 30, 0, tzinfo=<UTC>)

# Convert to different timezone (in application code)
import pytz
br_tz = pytz.timezone('America/Sao_Paulo')
local_time = assessment.created_at.astimezone(br_tz)
```

## 12. UUID Handling

```python
import uuid

# Manual UUID
user_id = uuid.uuid4()  # or use model's auto-generated

# Query by UUID
user = session.query(User).filter(User.id == user_id).first()

# UUID in JSON
assessment.metadata = {
    "user_uuid": str(user_id),
    "session_id": str(uuid.uuid4())
}
```

## 13. JSON Fields

```python
# Store any JSON-serializable data
question.metadata = {
    "options": ["A", "B", "C"],
    "scoring_rules": {
        "A": {"disc_d": 1.0},
        "B": {"disc_c": 1.0}
    },
    "weights": [0.5, 0.3, 0.2]
}

# Access nested data
options = question.metadata.get("options")
scoring = question.metadata["scoring_rules"].get("A")

# Update
question.metadata["updated"] = True
session.commit()
```

## 14. Numeric Precision

```python
from decimal import Decimal

# All scores are Numeric(5, 2) - 999.99 max, 2 decimals
# Use Decimal for exact arithmetic
result.disc_d = Decimal("72.50")
result.disc_i = Decimal("58.30")

# Sum check
total = sum([
    float(result.disc_d),
    float(result.disc_i),
    float(result.disc_s),
    float(result.disc_c)
])  # Should be ~100
```

## 15. Eager Loading

```python
from sqlalchemy.orm import joinedload

# Avoid N+1 queries
users = session.query(User).options(
    joinedload(User.assessments),
    joinedload(User.results)
).all()

# Access without additional queries
for user in users:
    for assessment in user.assessments:
        print(assessment.status)
```

---

## Database Statistics

```python
# Count users
user_count = session.query(User).count()

# Count assessments by status
from sqlalchemy import func
status_stats = session.query(
    Assessment.status,
    func.count(Assessment.id)
).group_by(Assessment.status).all()

# Average completion time
from sqlalchemy import func
avg_duration = session.query(
    func.avg(
        Assessment.completed_at - Assessment.started_at
    )
).filter(
    Assessment.status == "completed"
).scalar()
```

---

Generated: 2024-03-12
Models Location: /app/models/
