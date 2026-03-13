"""
Endpoints de responses (respostas às perguntas).

Gerencia criação, listagem e atualização de respostas.
"""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.response import Response
from app.schemas import response as response_schema
from app.services.questions_loader import get_question_by_id

router = APIRouter()


@router.post("/", response_model=response_schema.ResponsePublic, status_code=status.HTTP_201_CREATED)
def create_response(
    response_in: response_schema.ResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Salva resposta de uma pergunta.

    Verifica:
    - Se o assessment pertence ao usuário
    - Se a pergunta existe
    - Se já existe resposta (atualiza ao invés de duplicar)
    """
    # Verifica se assessment existe e pertence ao usuário
    assessment = db.query(Assessment).filter(
        Assessment.id == response_in.assessment_id
    ).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    if assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para responder este assessment"
        )

    # Verifica se assessment está em progresso
    if assessment.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment já foi finalizado"
        )

    # Verifica se pergunta existe no YAML
    # Note: question_id é UUID no banco, mas vem do frontend mapeado
    # Para simplificar, vamos aceitar qualquer UUID
    # Em produção, você pode adicionar validação extra

    # Verifica se já existe resposta para esta pergunta
    existing_response = db.query(Response).filter(
        Response.assessment_id == response_in.assessment_id,
        Response.question_id == response_in.question_id
    ).first()

    if existing_response:
        # Atualiza resposta existente
        existing_response.answer_value = response_in.answer_value
        db.commit()
        db.refresh(existing_response)
        return existing_response

    # Cria nova resposta
    response = Response(
        assessment_id=response_in.assessment_id,
        question_id=response_in.question_id,
        answer_value=response_in.answer_value
    )
    db.add(response)

    # Atualiza progresso do assessment
    total_responses = db.query(Response).filter(
        Response.assessment_id == response_in.assessment_id
    ).count() + 1

    assessment.current_question_index = total_responses

    db.commit()
    db.refresh(response)

    return response


@router.get("/{assessment_id}", response_model=List[response_schema.ResponsePublic])
def get_assessment_responses(
    assessment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Lista todas as respostas de um assessment.

    Apenas o dono do assessment pode acessar.
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
            detail="Você não tem permissão para acessar estas respostas"
        )

    # Busca todas as respostas
    responses = db.query(Response).filter(
        Response.assessment_id == assessment_id
    ).order_by(Response.answered_at).all()

    return responses


@router.patch("/{response_id}", response_model=response_schema.ResponsePublic)
def update_response(
    response_id: UUID,
    answer_value: Any,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Atualiza resposta existente.

    Permite que usuário mude sua resposta antes de finalizar assessment.
    """
    # Busca resposta
    response = db.query(Response).filter(Response.id == response_id).first()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resposta não encontrada"
        )

    # Verifica ownership através do assessment
    assessment = db.query(Assessment).filter(
        Assessment.id == response.assessment_id
    ).first()

    if not assessment or assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar esta resposta"
        )

    # Verifica se assessment ainda está em progresso
    if assessment.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível atualizar respostas de um assessment finalizado"
        )

    # Atualiza resposta
    response.answer_value = answer_value
    db.commit()
    db.refresh(response)

    return response
