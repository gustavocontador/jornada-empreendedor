"""
Router principal da API v1.

Agrega todos os endpoints em /api/v1.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    assessments,
    questions,
    responses,
    results,
    reports,
    admin
)

# Router principal v1
api_router = APIRouter()

# Inclui todos os routers com seus prefixos e tags
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

api_router.include_router(
    assessments.router,
    prefix="/assessments",
    tags=["Assessments"]
)

api_router.include_router(
    questions.router,
    prefix="/questions",
    tags=["Perguntas"]
)

api_router.include_router(
    responses.router,
    prefix="/responses",
    tags=["Respostas"]
)

api_router.include_router(
    results.router,
    prefix="/results",
    tags=["Resultados"]
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Relatórios"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Administração"]
)
