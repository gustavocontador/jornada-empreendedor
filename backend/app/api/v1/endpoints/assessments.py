"""
Endpoints de assessments (avaliações).

Gerencia criação, listagem e finalização de assessments.
"""
from datetime import datetime
from typing import Any
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.response import Response
from app.models.result import Result
from app.models.question import Question
from app.schemas import assessment as assessment_schema
from app.services.calculators.scoring_engine import ScoringEngine
from app.services.questions_loader import get_questions_data

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/current", response_model=assessment_schema.AssessmentPublic)
def get_current_assessment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna o assessment em progresso do usuário logado.

    Se não houver assessment em progresso, retorna 404.
    """
    assessment = db.query(Assessment).filter(
        Assessment.user_id == current_user.id,
        Assessment.status == "in_progress"
    ).order_by(Assessment.created_at.desc()).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum assessment em progresso encontrado"
        )

    return assessment


@router.post("/", response_model=assessment_schema.AssessmentPublic, status_code=status.HTTP_201_CREATED)
def create_assessment(
    assessment_in: assessment_schema.AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Inicia novo assessment para o usuário logado.
    """
    # Carrega dados das perguntas para obter total
    questions_data = get_questions_data()
    total_questions = len(questions_data.get("perguntas", []))

    # Cria novo assessment
    assessment = Assessment(
        user_id=current_user.id,
        status="in_progress",
        current_question_index=0,
        total_questions=total_questions,
        extra_data=assessment_in.metadata or {}
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


@router.get("/{assessment_id}", response_model=assessment_schema.AssessmentPublic)
def get_assessment(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna assessment específico.

    Apenas o dono do assessment pode acessá-lo.
    """
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    # Verifica ownership
    if assessment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este assessment"
        )

    return assessment


@router.post("/{assessment_id}/complete", response_model=dict)
def complete_assessment(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Finaliza assessment e calcula todos os scores.

    Cria registro em 'results' com todos os frameworks calculados.
    """
    logger.info(
        "Iniciando finalização de assessment",
        extra={
            "assessment_id": str(assessment_id),
            "user_id": str(current_user.id),
            "user_email": current_user.email
        }
    )

    # Busca assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        logger.warning(
            "Assessment não encontrado",
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
            "total_questions": assessment.total_questions
        }
    )

    # Verifica ownership
    logger.info(
        "Verificando ownership",
        extra={
            "assessment_user_id": str(assessment.user_id),
            "current_user_id": str(current_user.id)
        }
    )
    if assessment.user_id != current_user.id:
        logger.warning(
            "Tentativa de acesso não autorizado",
            extra={
                "assessment_id": str(assessment_id),
                "assessment_owner": str(assessment.user_id),
                "requesting_user": str(current_user.id)
            }
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este assessment"
        )

    # Verifica se já foi completado
    logger.info(
        "Verificando status do assessment",
        extra={"status": assessment.status}
    )
    if assessment.status == "completed":
        logger.warning(
            "Assessment já completado",
            extra={"assessment_id": str(assessment_id)}
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment já foi finalizado"
        )

    # Busca todas as respostas do assessment (com eager load de Question para scoring)
    logger.info(
        "Buscando respostas do assessment",
        extra={"assessment_id": str(assessment_id)}
    )
    from sqlalchemy.orm import joinedload
    responses = db.query(Response).options(
        joinedload(Response.question)
    ).filter(
        Response.assessment_id == assessment_id
    ).all()

    logger.info(
        "Respostas carregadas",
        extra={
            "assessment_id": str(assessment_id),
            "responses_count": len(responses),
            "expected_count": assessment.total_questions
        }
    )

    # Verifica se tem respostas suficientes
    if len(responses) < assessment.total_questions:
        # Identifica quais perguntas não foram respondidas
        questions_data = get_questions_data()
        all_question_ids = [q.get("id") for q in questions_data.get("perguntas", [])]

        # Busca os IDs YAML das respostas salvas
        answered_ids = []
        for response in responses:
            question = db.query(Question).filter(Question.id == response.question_id).first()
            if question and question.extra_data:
                yaml_id = question.extra_data.get("id")
                if yaml_id:
                    answered_ids.append(yaml_id)

        # Identifica perguntas faltantes
        missing_questions = [qid for qid in all_question_ids if qid not in answered_ids]

        logger.warning(
            "Assessment incompleto",
            extra={
                "assessment_id": str(assessment_id),
                "responses_count": len(responses),
                "expected_count": assessment.total_questions,
                "missing_questions": missing_questions
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assessment incompleto. Respondidas {len(responses)}/{assessment.total_questions} perguntas. Faltam: {', '.join(missing_questions)}"
        )

    # Carrega dados das perguntas
    logger.info("Carregando dados das perguntas do YAML")
    questions_data = get_questions_data()

    # Calcula todos os scores usando o ScoringEngine
    try:
        logger.info("Iniciando cálculo de scores")
        scores = ScoringEngine.calculate_all_scores(responses, questions_data)
        logger.info(
            "Scores calculados com sucesso",
            extra={"assessment_id": str(assessment_id)}
        )
    except Exception as e:
        logger.error(
            "Erro ao calcular scores",
            exc_info=True,
            extra={
                "assessment_id": str(assessment_id),
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao calcular scores: {str(e)}"
        ) from e

    # Verifica se já existe resultado
    existing_result = db.query(Result).filter(
        Result.assessment_id == assessment_id
    ).first()

    if existing_result:
        # Atualiza resultado existente
        logger.info(
            "Atualizando resultado existente",
            extra={
                "assessment_id": str(assessment_id),
                "result_id": str(existing_result.id)
            }
        )
        existing_result.scores = scores
        existing_result.calculated_at = datetime.utcnow()
    else:
        # Cria novo resultado
        logger.info(
            "Criando novo resultado",
            extra={"assessment_id": str(assessment_id)}
        )
        result = Result(
            user_id=current_user.id,
            assessment_id=assessment_id,
            scores=scores
        )
        db.add(result)

    # Atualiza assessment
    logger.info(
        "Atualizando status do assessment para 'completed'",
        extra={"assessment_id": str(assessment_id)}
    )
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    assessment.current_question_index = assessment.total_questions

    try:
        logger.info("Commitando alterações no banco de dados")
        db.commit()
        db.refresh(assessment)
        logger.info(
            "Assessment finalizado com sucesso",
            extra={
                "assessment_id": str(assessment.id),
                "user_id": str(current_user.id),
                "completed_at": assessment.completed_at.isoformat()
            }
        )
    except Exception as e:
        logger.error(
            "Erro ao commitar alterações no banco de dados",
            exc_info=True,
            extra={
                "assessment_id": str(assessment_id),
                "error": str(e)
            }
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar resultados: {str(e)}"
        ) from e

    return {
        "message": "Assessment finalizado com sucesso",
        "assessment_id": str(assessment.id),
        "status": "completed",
        "scores_calculated": True
    }


@router.get("/", response_model=list[assessment_schema.AssessmentPublic])
def list_my_assessments(
    skip: int = 0,
    limit: int = 20,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Lista todos os assessments do usuário logado.

    Suporta paginação e filtro por status.
    """
    query = db.query(Assessment).filter(Assessment.user_id == current_user.id)

    # Filtro por status (opcional)
    if status_filter:
        if status_filter not in ["in_progress", "completed", "abandoned"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status inválido. Use: in_progress, completed ou abandoned"
            )
        query = query.filter(Assessment.status == status_filter)

    # Ordena por mais recente
    query = query.order_by(Assessment.created_at.desc())

    # Paginação
    assessments = query.offset(skip).limit(limit).all()

    return assessments
