"""
Schemas Pydantic para Result (Resultado da avaliação).
"""
from datetime import datetime
from typing import Optional, Any
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field


class DISCScores(BaseModel):
    """Scores do framework DISC."""
    d: Decimal = Field(..., ge=0, le=100, description="Dominância")
    i: Decimal = Field(..., ge=0, le=100, description="Influência")
    s: Decimal = Field(..., ge=0, le=100, description="Estabilidade")
    c: Decimal = Field(..., ge=0, le=100, description="Conformidade")
    profile: str = Field(..., description="Perfil DISC (ex: DI, SC, DIS)")


class SpiralScores(BaseModel):
    """Scores do framework Spiral Dynamics."""
    beige: Decimal = Field(default=0, ge=0, le=100, description="Instinto")
    purple: Decimal = Field(default=0, ge=0, le=100, description="Tribal")
    red: Decimal = Field(default=0, ge=0, le=100, description="Impulsivo/Poder")
    blue: Decimal = Field(default=0, ge=0, le=100, description="Tradicional/Ordem")
    orange: Decimal = Field(default=0, ge=0, le=100, description="Moderno/Conquista")
    green: Decimal = Field(default=0, ge=0, le=100, description="Pós-moderno/Igualitário")
    yellow: Decimal = Field(default=0, ge=0, le=100, description="Integrador/Sistêmico")
    turquoise: Decimal = Field(default=0, ge=0, le=100, description="Holístico/Global")
    primary: str = Field(..., description="Nível primário")
    secondary: Optional[str] = Field(None, description="Nível secundário")
    tertiary: Optional[str] = Field(None, description="Nível terciário")


class PAEIScores(BaseModel):
    """Scores do framework PAEI (Adizes)."""
    p: Decimal = Field(..., ge=0, le=100, description="Produtor")
    a: Decimal = Field(..., ge=0, le=100, description="Administrador")
    e: Decimal = Field(..., ge=0, le=100, description="Empreendedor")
    i: Decimal = Field(..., ge=0, le=100, description="Integrador")
    code: str = Field(..., description="Código PAEI (ex: PAeI, paEi)")


class EnneagramScores(BaseModel):
    """Scores do framework Eneagrama."""
    type: int = Field(..., ge=1, le=9, description="Tipo do Eneagrama (1-9)")
    wing: Optional[str] = Field(None, description="Asa (ex: 8w9, 3w4)")
    subtype: Optional[str] = Field(
        None,
        pattern="^(sp|so|sx|self-preservation|social|sexual)$",
        description="Subtipo instintivo"
    )


class ValoresScores(BaseModel):
    """Scores de Valores Empresariais."""
    primary: str = Field(..., description="Valor primário")
    secondary: Optional[str] = Field(None, description="Valor secundário")
    tertiary: Optional[str] = Field(None, description="Valor terciário")


class ArquetiposScores(BaseModel):
    """Scores de Arquétipos de Contratação."""
    primary: str = Field(..., description="Arquétipo primário")
    secondary: Optional[str] = Field(None, description="Arquétipo secundário")
    tertiary: Optional[str] = Field(None, description="Arquétipo terciário")


class ResultComplete(BaseModel):
    """Resultado completo da avaliação com todos os frameworks."""
    id: UUID
    assessment_id: UUID
    user_id: UUID

    # Frameworks
    disc: DISCScores
    spiral: SpiralScores
    paei: PAEIScores
    enneagram: EnneagramScores
    valores: ValoresScores
    arquetipos: ArquetiposScores

    # Interpretações e recomendações
    interpretations: dict[str, Any] = Field(
        ...,
        description="Interpretações profundas baseadas nos resultados"
    )
    recommendations: dict[str, Any] = Field(
        ...,
        description="Recomendações personalizadas"
    )

    created_at: datetime

    class Config:
        from_attributes = True


class ResultPublic(BaseModel):
    """Resultado completo da avaliação."""
    id: UUID
    assessment_id: UUID
    user_id: UUID

    # Scores completos (armazenados como JSON no banco)
    scores: dict[str, Any] = Field(
        ...,
        description="Todos os scores calculados (DISC, Spiral, PAEI, etc.)"
    )

    calculated_at: datetime

    class Config:
        from_attributes = True
