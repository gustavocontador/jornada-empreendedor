"""
Schemas Pydantic para Assessment (Avaliação).
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class AssessmentBase(BaseModel):
    """Schema base de avaliação."""
    pass


class AssessmentCreate(BaseModel):
    """Schema para criação de avaliação."""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class AssessmentUpdate(BaseModel):
    """Schema para atualização de avaliação."""
    status: Optional[str] = Field(None, pattern="^(in_progress|completed|abandoned)$")
    current_question_index: Optional[int] = Field(None, ge=0, le=105)
    completed_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class AssessmentInDB(BaseModel):
    """Schema de avaliação como armazenado no banco."""
    id: UUID
    user_id: UUID
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    current_question_index: int
    total_questions: int
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssessmentPublic(BaseModel):
    """Schema de avaliação para resposta pública (com progresso calculado)."""
    id: UUID
    user_id: UUID
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    current_question_index: int
    total_questions: int
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def progress_percentage(self) -> float:
        """Calcula porcentagem de progresso."""
        if self.total_questions == 0:
            return 0.0
        return round((self.current_question_index / self.total_questions) * 100, 2)

    class Config:
        from_attributes = True
