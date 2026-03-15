"""
Schemas Pydantic para Response (Resposta a questão).
"""
from datetime import datetime
from typing import Any, Union
from uuid import UUID

from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    """Schema base de resposta."""
    answer_value: Union[int, str, list[str], dict[str, Any]] = Field(
        ...,
        description="Valor da resposta (pode ser número, string, array ou objeto)"
    )


class ResponseCreate(ResponseBase):
    """Schema para criação de resposta."""
    assessment_id: UUID
    question_id: str  # ID da pergunta do YAML (ex: "q001")


class ResponseInDB(ResponseBase):
    """Schema de resposta como armazenado no banco."""
    id: UUID
    assessment_id: UUID
    question_id: UUID
    answered_at: datetime

    class Config:
        from_attributes = True


class ResponsePublic(BaseModel):
    """Schema de resposta para resposta pública."""
    id: UUID
    assessment_id: UUID
    question_id: str  # Retorna como ID do YAML (ex: "q001")
    answer_value: Union[int, str, list[str], dict[str, Any]]
    answered_at: datetime

    class Config:
        from_attributes = True
