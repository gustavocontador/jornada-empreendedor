"""
Modelo Report - Relatório gerado a partir dos resultados da avaliação.
"""
from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Report(Base):
    """
    Modelo de relatório.

    Representa um relatório gerado a partir dos resultados da avaliação.
    Pode ser simplificado ou completo, e pode ser exportado em PDF.
    """
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    result_id = Column(UUID(as_uuid=True), ForeignKey("results.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(String(50), nullable=False, index=True)  # simplified, complete
    pdf_path = Column(String(500), nullable=True)  # Caminho do PDF gerado
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    extra_data = Column(JSON, default=dict, nullable=False)  # Informações adicionais (versão, idioma, etc)

    # Relationships
    result = relationship("Result", back_populates="reports")
    user = relationship("User", back_populates="reports")

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, result_id={self.result_id}, type={self.report_type})>"
