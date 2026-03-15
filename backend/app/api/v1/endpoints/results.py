"""
Endpoints de results (resultados calculados).

Retorna scores calculados de assessments finalizados.
"""
from typing import Any
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.result import Result
from app.schemas import result as result_schema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{assessment_id}", response_model=dict)
def get_results(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna resultados completos de um assessment formatados para o frontend.

    Inclui todos os scores de todos os frameworks.
    """
    logger.info(
        "Buscando resultados de assessment",
        extra={
            "assessment_id": str(assessment_id),
            "user_id": str(current_user.id),
            "user_email": current_user.email
        }
    )

    # Verifica se assessment existe e pertence ao usuário
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        logger.warning(
            "Assessment não encontrado ao buscar resultados",
            extra={"assessment_id": str(assessment_id)}
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    logger.info(
        "Assessment encontrado",
        extra={
            "assessment_id": str(assessment_id),
            "status": assessment.status,
            "owner_id": str(assessment.user_id)
        }
    )

    if assessment.user_id != current_user.id and not current_user.is_admin:
        logger.warning(
            "Tentativa de acesso não autorizado aos resultados",
            extra={
                "assessment_id": str(assessment_id),
                "assessment_owner": str(assessment.user_id),
                "requesting_user": str(current_user.id)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar estes resultados"
        )

    # Verifica se assessment foi completado
    if assessment.status != "completed":
        logger.warning(
            "Tentativa de buscar resultados de assessment não completado",
            extra={
                "assessment_id": str(assessment_id),
                "current_status": assessment.status
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment ainda não foi finalizado. Complete todas as perguntas primeiro."
        )

    # Busca resultado
    result = db.query(Result).filter(
        Result.assessment_id == assessment_id
    ).first()

    if not result:
        logger.error(
            "Resultado não encontrado para assessment completado",
            extra={
                "assessment_id": str(assessment_id),
                "assessment_status": assessment.status,
                "completed_at": assessment.completed_at.isoformat() if assessment.completed_at else None
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultados não encontrados. Execute POST /assessments/{id}/complete primeiro."
        )

    logger.info(
        "Resultado encontrado, formatando resposta",
        extra={
            "assessment_id": str(assessment_id),
            "result_id": str(result.id),
            "calculated_at": result.calculated_at.isoformat()
        }
    )

    scores = result.scores

    # Formata dados para o formato esperado pelo frontend
    try:
        formatted_result = {
            "id": str(result.id),
            "assessmentId": str(result.assessment_id),
            "userId": str(result.user_id),
        "disc": {
            "D": scores.get("disc", {}).get("d", 50),
            "I": scores.get("disc", {}).get("i", 50),
            "S": scores.get("disc", {}).get("s", 50),
            "C": scores.get("disc", {}).get("c", 50),
            "profile": scores.get("disc", {}).get("profile", "disc"),
            "description": scores.get("disc", {}).get("description", "")
        },
        "spiral_dynamics": {
            "beige": scores.get("spiral", {}).get("beige", 0),
            "purple": scores.get("spiral", {}).get("purple", 0),
            "red": scores.get("spiral", {}).get("red", 0),
            "blue": scores.get("spiral", {}).get("blue", 0),
            "orange": scores.get("spiral", {}).get("orange", 0),
            "green": scores.get("spiral", {}).get("green", 0),
            "yellow": scores.get("spiral", {}).get("yellow", 0),
            "turquoise": scores.get("spiral", {}).get("turquoise", 0),
            "dominant_color": scores.get("spiral", {}).get("primary", "beige"),
            "description": scores.get("spiral", {}).get("description", "")
        },
        "paei": {
            "P": scores.get("paei", {}).get("p", 50),
            "A": scores.get("paei", {}).get("a", 50),
            "E": scores.get("paei", {}).get("e", 50),
            "I": scores.get("paei", {}).get("i", 50),
            "code": scores.get("paei", {}).get("code", "paei"),
            "description": scores.get("paei", {}).get("description", "")
        },
        "enneagram": {
            "type": scores.get("enneagram", {}).get("type", 1),
            "wing": scores.get("enneagram", {}).get("wing"),
            "description": scores.get("enneagram", {}).get("description", ""),
            "strengths": scores.get("enneagram", {}).get("insights", [])[:3],
            "challenges": scores.get("interpretations", {}).get("desafios", [])[:3]
        },
        "values": {
            "top_values": [
                scores.get("valores", {}).get("primary", ""),
                scores.get("valores", {}).get("secondary", ""),
                scores.get("valores", {}).get("tertiary", "")
            ],
            "descriptions": {
                scores.get("valores", {}).get("primary", ""): scores.get("valores", {}).get("description", ""),
                scores.get("valores", {}).get("secondary", ""): "",
                scores.get("valores", {}).get("tertiary", ""): ""
            }
        },
            "overall_summary": scores.get("interpretations", {}).get("perfil_geral", "Seu perfil completo foi calculado com sucesso."),
            "recommendations": _extract_recommendations(scores.get("recommendations", {})),
            "createdAt": result.calculated_at.isoformat(),
            "updatedAt": result.calculated_at.isoformat()
        }

        logger.info(
            "Resultados formatados e retornados com sucesso",
            extra={
                "assessment_id": str(assessment_id),
                "result_id": str(result.id)
            }
        )

        return formatted_result

    except Exception as e:
        logger.error(
            "Erro ao formatar resultados",
            exc_info=True,
            extra={
                "assessment_id": str(assessment_id),
                "result_id": str(result.id) if result else None,
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao formatar resultados: {str(e)}"
        ) from e


def _extract_recommendations(recommendations: dict) -> list:
    """Extrai recomendações de todas as categorias."""
    all_recs = []
    for _category, recs in recommendations.items():
        for rec in recs:
            if isinstance(rec, dict):
                all_recs.append(rec.get("recommendation", rec.get("action", str(rec))))
            else:
                all_recs.append(str(rec))
    return all_recs[:10]  # Limita a 10 recomendações


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
