"""
Endpoints de results (resultados calculados).

Retorna scores calculados de assessments finalizados.
"""
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.result import Result
from app.schemas import result as result_schema

router = APIRouter()


@router.get("/{assessment_id}", response_model=result_schema.ResultPublic)
def get_results(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna resultados completos de um assessment.

    Inclui todos os scores de todos os frameworks.
    """
    # Verifica se assessment existe e pertence ao usuário
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    if assessment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar estes resultados"
        )

    # Verifica se assessment foi completado
    if assessment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment ainda não foi finalizado. Complete todas as perguntas primeiro."
        )

    # Busca resultado
    result = db.query(Result).filter(
        Result.assessment_id == assessment_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultados não encontrados. Execute POST /assessments/{id}/complete primeiro."
        )

    return result


@router.get("/{assessment_id}/summary", response_model=dict)
def get_results_summary(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna resumo simplificado dos resultados.

    Inclui apenas os highlights principais de cada framework.
    """
    # Verifica se assessment existe e pertence ao usuário
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    if assessment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar estes resultados"
        )

    # Verifica se assessment foi completado
    if assessment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment ainda não foi finalizado"
        )

    # Busca resultado
    result = db.query(Result).filter(
        Result.assessment_id == assessment_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultados não encontrados"
        )

    scores = result.scores

    # Extrai apenas os principais de cada framework
    summary = {
        "assessment_id": str(assessment_id),
        "calculated_at": result.calculated_at,
        "disc": {
            "profile": scores.get("disc", {}).get("profile"),
            "primary": scores.get("disc", {}).get("primary"),
            "description": scores.get("disc", {}).get("description")
        },
        "spiral": {
            "primary": scores.get("spiral", {}).get("primary"),
            "secondary": scores.get("spiral", {}).get("secondary"),
            "description": scores.get("spiral", {}).get("description")
        },
        "paei": {
            "code": scores.get("paei", {}).get("code"),
            "style": scores.get("paei", {}).get("style"),
            "description": scores.get("paei", {}).get("description")
        },
        "enneagram": {
            "type": scores.get("enneagram", {}).get("type"),
            "wing": scores.get("enneagram", {}).get("wing"),
            "description": scores.get("enneagram", {}).get("description")
        },
        "valores": {
            "primary": scores.get("valores", {}).get("primary"),
            "secondary": scores.get("valores", {}).get("secondary"),
            "tertiary": scores.get("valores", {}).get("tertiary")
        },
        "arquetipos": {
            "primary": scores.get("arquetipos", {}).get("primary"),
            "secondary": scores.get("arquetipos", {}).get("secondary"),
            "tertiary": scores.get("arquetipos", {}).get("tertiary")
        },
        "key_strengths": scores.get("interpretations", {}).get("key_strengths", [])[:3],
        "key_challenges": scores.get("interpretations", {}).get("key_challenges", [])[:3],
        "top_recommendations": [
            rec for category in scores.get("recommendations", {}).values()
            for rec in category
            if rec.get("priority") in ["critical", "high"]
        ][:5]
    }

    return summary
