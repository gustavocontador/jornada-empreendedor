"""
Modelo Result - Resultado calculado da avaliação com todos os scores.
"""
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Result(Base):
    """
    Modelo de resultado da avaliação.

    Contém todos os scores calculados a partir das respostas:
    - DISC (Dominância, Influência, Estabilidade, Conformidade)
    - Spiral Dynamics (8 níveis de desenvolvimento)
    - PAEI (4 papéis organizacionais)
    - Enneagrama (9 tipos de personalidade)
    - Valores principais
    - Arquetipos de liderança
    - Interpretações e recomendações
    """
    __tablename__ = "results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Scores completos (todos os frameworks) armazenados como JSON
    scores = Column(JSON, nullable=False)

    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, name="created_at")

    # Relationships
    assessment = relationship("Assessment", back_populates="result")
    user = relationship("User", back_populates="results")
    reports = relationship("Report", back_populates="result", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Result(id={self.id}, assessment_id={self.assessment_id})>"
