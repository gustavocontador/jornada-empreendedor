"""
Schemas Pydantic para Response (Resposta a questão).
"""
from datetime import datetime
from typing import Dict, Any, Union, List
from uuid import UUID

from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    """Schema base de resposta."""
    answer_value: Union[int, str, List[str], Dict[str, Any]] = Field(
        ...,
        description="Valor da resposta (pode ser número, string, array ou objeto)"
    )


class ResponseCreate(ResponseBase):
    """Schema para criação de resposta."""
    assessment_id: UUID
    question_id: UUID


class ResponseInDB(ResponseBase):
    """Schema de resposta como armazenado no banco."""
    id: UUID
    assessment_id: UUID
    question_id: UUID
    answered_at: datetime

    class Config:
        from_attributes = True


class ResponsePublic(ResponseInDB):
    """Schema de resposta para resposta pública."""
    pass
