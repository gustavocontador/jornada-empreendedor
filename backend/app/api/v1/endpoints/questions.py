"""
Endpoints de questions (perguntas do questionário).

Retorna perguntas carregadas do YAML.
"""
from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.services.questions_loader import (
    get_questions_data,
    get_question_by_id,
    get_questions_by_section,
    get_sections
)

router = APIRouter()


@router.get("/", response_model=dict)
def list_questions(
    skip: int = Query(0, ge=0, description="Número de perguntas para pular (paginação)"),
    limit: int = Query(20, ge=1, le=105, description="Número máximo de perguntas a retornar"),
    section: Optional[str] = Query(None, description="Filtrar por seção (intro, comportamento_valores, etc.)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Lista perguntas do questionário.

    Suporta:
    - Paginação (skip/limit)
    - Filtro por seção
    """
    questions_data = get_questions_data()
    all_questions = questions_data.get("perguntas", [])

    # Filtro por seção (opcional)
    if section:
        filtered_questions = [q for q in all_questions if q.get("secao") == section]
        if not filtered_questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Seção '{section}' não encontrada"
            )
        questions = filtered_questions
    else:
        questions = all_questions

    # Paginação
    total = len(questions)
    paginated_questions = questions[skip:skip + limit]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "section": section,
        "questions": paginated_questions,
        "metadata": questions_data.get("metadata", {})
    }


@router.get("/sections", response_model=list[dict])
def list_sections(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Lista todas as seções do questionário.
    """
    sections = get_sections()
    if not sections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma seção encontrada"
        )
    return sections


@router.get("/{question_id}", response_model=dict)
def get_question(
    question_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna pergunta específica por ID.

    O question_id deve ser no formato 'q001', 'q002', etc.
    """
    question = get_question_by_id(question_id)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pergunta '{question_id}' não encontrada"
        )

    return question
