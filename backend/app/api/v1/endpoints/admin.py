"""
Endpoints administrativos.

Apenas para usuários com is_admin=True.
"""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_admin_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.result import Result
from app.models.report import Report
from app.schemas import user as user_schema
from app.schemas import assessment as assessment_schema

router = APIRouter()


@router.get("/users", response_model=List[user_schema.UserPublic])
def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
) -> Any:
    """
    Lista todos os usuários do sistema.

    Apenas admins.
    """
    users = db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users


@router.get("/assessments", response_model=List[assessment_schema.AssessmentPublic])
def list_all_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: str = Query(None),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
) -> Any:
    """
    Lista todos os assessments do sistema.

    Apenas admins. Suporta filtro por status.
    """
    query = db.query(Assessment)

    if status_filter:
        if status_filter not in ["in_progress", "completed", "abandoned"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status inválido"
            )
        query = query.filter(Assessment.status == status_filter)

    assessments = query.order_by(Assessment.created_at.desc()).offset(skip).limit(limit).all()
    return assessments


@router.get("/dashboard", response_model=dict)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
) -> Any:
    """
    Retorna dashboard administrativo com estatísticas do sistema.

    Apenas admins.
    """
    # Total de usuários
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()

    # Total de assessments por status
    total_assessments = db.query(func.count(Assessment.id)).scalar()
    completed_assessments = db.query(func.count(Assessment.id)).filter(
        Assessment.status == "completed"
    ).scalar()
    in_progress_assessments = db.query(func.count(Assessment.id)).filter(
        Assessment.status == "in_progress"
    ).scalar()

    # Total de resultados calculados
    total_results = db.query(func.count(Result.id)).scalar()

    # Total de relatórios gerados
    total_reports = db.query(func.count(Report.id)).scalar()
    completed_reports = db.query(func.count(Report.id)).filter(
        Report.status == "completed"
    ).scalar()

    # Taxa de conclusão
    completion_rate = 0.0
    if total_assessments > 0:
        completion_rate = round((completed_assessments / total_assessments) * 100, 2)

    # Usuários mais ativos (mais assessments)
    top_users = db.query(
        User.id,
        User.email,
        User.full_name,
        func.count(Assessment.id).label("assessment_count")
    ).join(Assessment).group_by(User.id).order_by(
        func.count(Assessment.id).desc()
    ).limit(5).all()

    top_users_data = [
        {
            "user_id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "assessment_count": user.assessment_count
        }
        for user in top_users
    ]

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users
        },
        "assessments": {
            "total": total_assessments,
            "completed": completed_assessments,
            "in_progress": in_progress_assessments,
            "completion_rate": completion_rate
        },
        "results": {
            "total": total_results
        },
        "reports": {
            "total": total_reports,
            "completed": completed_reports
        },
        "top_users": top_users_data
    }


@router.post("/users/{user_id}/toggle-active", response_model=user_schema.UserPublic)
def toggle_user_active(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
) -> Any:
    """
    Ativa/desativa um usuário.

    Apenas admins. Não pode desativar o próprio usuário.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    # Impede admin de desativar a si mesmo
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode desativar sua própria conta"
        )

    # Toggle
    user.is_active = not user.is_active

    db.commit()
    db.refresh(user)

    return user
