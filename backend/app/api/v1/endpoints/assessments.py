"""
Endpoints de assessments (avaliações).

Gerencia criação, listagem e finalização de assessments.
"""
from datetime import datetime
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.response import Response
from app.models.result import Result
from app.schemas import assessment as assessment_schema
from app.services.calculators.scoring_engine import ScoringEngine
from app.services.questions_loader import get_questions_data

router = APIRouter()


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
        metadata=assessment_in.metadata or {}
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
    # Busca assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    # Verifica ownership
    if assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este assessment"
        )

    # Verifica se já foi completado
    if assessment.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment já foi finalizado"
        )

    # Busca todas as respostas do assessment
    responses = db.query(Response).filter(
        Response.assessment_id == assessment_id
    ).all()

    # Verifica se tem respostas suficientes
    if len(responses) < assessment.total_questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assessment incompleto. Respondidas {len(responses)}/{assessment.total_questions} perguntas."
        )

    # Carrega dados das perguntas
    questions_data = get_questions_data()

    # Calcula todos os scores usando o ScoringEngine
    try:
        scores = ScoringEngine.calculate_all_scores(responses, questions_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao calcular scores: {str(e)}"
        )

    # Verifica se já existe resultado
    existing_result = db.query(Result).filter(
        Result.assessment_id == assessment_id
    ).first()

    if existing_result:
        # Atualiza resultado existente
        existing_result.scores = scores
        existing_result.calculated_at = datetime.utcnow()
    else:
        # Cria novo resultado
        result = Result(
            user_id=current_user.id,
            assessment_id=assessment_id,
            scores=scores
        )
        db.add(result)

    # Atualiza assessment
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    assessment.current_question_index = assessment.total_questions

    db.commit()
    db.refresh(assessment)

    return {
        "message": "Assessment finalizado com sucesso",
        "assessment_id": str(assessment.id),
        "status": "completed",
        "scores_calculated": True
    }


@router.get("/", response_model=List[assessment_schema.AssessmentPublic])
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
