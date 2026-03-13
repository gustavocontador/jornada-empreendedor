"""
Schemas Pydantic para Report (Relatório).
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class ReportBase(BaseModel):
    """Schema base de relatório."""
    report_type: str = Field(..., pattern="^(simplified|complete)$")


class ReportCreate(ReportBase):
    """Schema para criação de relatório."""
    assessment_id: UUID
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ReportInDB(ReportBase):
    """Schema de relatório como armazenado no banco."""
    id: UUID
    assessment_id: UUID
    user_id: UUID
    status: str
    file_path: Optional[str]
    created_at: datetime
    metadata: Dict[str, Any]

    class Config:
        from_attributes = True


class ReportPublic(ReportInDB):
    """Schema de relatório para resposta pública (com download URL)."""

    @computed_field
    @property
    def download_url(self) -> Optional[str]:
        """Gera URL de download do PDF."""
        if self.file_path:
            return f"/api/v1/reports/{self.id}/download"
        return None

    class Config:
        from_attributes = True
