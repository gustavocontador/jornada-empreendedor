"""
Modelo Question - Questões do questionário de avaliação.
"""
from datetime import datetime
from typing import List
import uuid

from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Question(Base):
    """
    Modelo de questão do questionário.

    Representa uma pergunta individual do questionário. Contém metadados sobre
    as opções de resposta, regras de pontuação e categoria (seção).
    """
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False, index=True)  # likert_5, multiple_choice, ranking, text
    section = Column(String(100), nullable=False, index=True)  # intro, comportamento_valores, lideranca, etc
    order_index = Column(Integer, nullable=False, index=True)  # Ordem de apresentação
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    metadata = Column(JSON, default=dict, nullable=False)  # opcoes, scoring_rules, etc
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    responses = relationship("Response", back_populates="question")

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, order={self.order_index}, type={self.question_type}, section={self.section})>"
