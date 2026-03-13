"""
Modelo Response - Resposta do usuário para uma questão.
"""
from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Response(Base):
    """
    Modelo de resposta a uma questão.

    Representa a resposta de um usuário para uma pergunta específica durante
    uma avaliação. Armazena o valor da resposta em formato JSON para suportar
    diferentes tipos de questões.
    """
    __tablename__ = "responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False, index=True)
    answer_value = Column(JSON, nullable=False)  # Suporta múltiplos formatos: número, string, array, objeto
    answered_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="responses")
    question = relationship("Question", back_populates="responses")

    def __repr__(self) -> str:
        return f"<Response(id={self.id}, assessment_id={self.assessment_id}, question_id={self.question_id})>"
