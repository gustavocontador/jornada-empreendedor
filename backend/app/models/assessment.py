"""
Modelo Assessment - Avaliação/Questionário respondido pelo usuário.
"""
from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Assessment(Base):
    """
    Modelo de avaliação/questionário.

    Representa uma sessão de preenchimento do questionário completo (105 questões).
    Rastreia o progresso da avaliação desde o início até a conclusão.
    """
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="in_progress", nullable=False, index=True)  # in_progress, completed, abandoned
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    current_question_index = Column(Integer, default=0, nullable=False)
    total_questions = Column(Integer, default=105, nullable=False)
    extra_data = Column(JSON, default=dict, nullable=False)  # Informações adicionais, contexto
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="assessments")
    responses = relationship("Response", back_populates="assessment", cascade="all, delete-orphan")
    result = relationship("Result", back_populates="assessment", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Assessment(id={self.id}, user_id={self.user_id}, status={self.status}, progress={self.current_question_index}/{self.total_questions})>"
