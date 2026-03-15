"""
Performance monitoring middleware.

Registra duração de requests e adiciona header X-Response-Time.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware para monitoramento de performance de requests."""

    async def dispatch(self, request: Request, call_next):
        """
        Processa request e mede tempo de execução.

        Args:
            request: Request do FastAPI
            call_next: Próximo middleware/handler

        Returns:
            Response com header X-Response-Time
        """
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time
        duration_ms = round(duration * 1000, 2)

        # Log estruturado da request
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "client_host": request.client.host if request.client else None,
            }
        )

        # Adiciona header de performance
        response.headers["X-Response-Time"] = f"{duration_ms}ms"

        return response
