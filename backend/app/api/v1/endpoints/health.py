"""
Health check endpoints para monitoramento e Kubernetes.

Endpoints:
- /health: Health check geral com verificação de database
- /health/ready: Readiness probe (Kubernetes)
- /health/live: Liveness probe (Kubernetes)
"""
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint para monitoramento.

    Verifica:
    - Status geral da aplicação
    - Conexão com database

    Returns:
        JSON com status da aplicação e serviços
    """
    db_status = "healthy"

    try:
        # Verifica conexão com database
        result = await db.execute(text("SELECT 1"))
        result.scalar()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        logger.error(
            "Database health check failed",
            exc_info=True,
            extra={"error": str(e)}
        )

    overall_status = "ok" if db_status == "healthy" else "degraded"

    return JSONResponse(
        status_code=status.HTTP_200_OK if overall_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": overall_status,
            "version": "1.0.0",
            "service": settings.PROJECT_NAME,
            "environment": settings.SENTRY_ENVIRONMENT,
            "checks": {
                "database": db_status,
            }
        }
    )


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Kubernetes readiness probe.

    Verifica se a aplicação está pronta para receber tráfego.
    Retorna 200 se pronto, 503 se não pronto.

    Returns:
        JSON com status de readiness
    """
    try:
        # Verifica se database está acessível
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"ready": True}
        )
    except Exception as e:
        logger.error(
            "Readiness check failed",
            exc_info=True,
            extra={"error": str(e)}
        )

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False, "reason": "database_unavailable"}
        )


@router.get("/health/live")
async def liveness_check():
    """
    Kubernetes liveness probe.

    Verifica se a aplicação está viva (não travada).
    Retorna sempre 200 se o processo está respondendo.

    Returns:
        JSON com status de liveness
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"alive": True}
    )
