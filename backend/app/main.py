"""
FastAPI Main Application.

Aplicação principal do backend "Jornada do Empreendedor de Sucesso".
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.services.questions_loader import get_questions_data

# Configuração de logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_default_admin(db: Session) -> None:
    """
    Cria usuário admin padrão se não existir.

    Email: admin@example.com
    Senha: admin123
    """
    admin_email = "admin@example.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if not existing_admin:
        admin = User(
            email=admin_email,
            full_name="Administrador",
            password_hash=get_password_hash("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        logger.info(f"✅ Usuário admin criado: {admin_email} / admin123")
    else:
        logger.info(f"✅ Usuário admin já existe: {admin_email}")


def load_questions_cache() -> None:
    """
    Carrega perguntas do YAML em cache na inicialização.
    """
    try:
        questions_data = get_questions_data()
        total = len(questions_data.get("perguntas", []))
        logger.info(f"✅ Perguntas carregadas em cache: {total} perguntas")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar perguntas: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events: startup e shutdown.
    """
    # Startup
    logger.info("🚀 Iniciando aplicação...")

    # Cria admin padrão
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()

    # Carrega perguntas em cache
    load_questions_cache()

    logger.info("✅ Aplicação iniciada com sucesso!")

    yield

    # Shutdown
    logger.info("👋 Encerrando aplicação...")


# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API para avaliação psicométrica de empreendedores",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de todas as requisições."""
    logger.info(f"📥 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code}")
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação do Pydantic."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join([str(loc) for loc in error["loc"]]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Erro de validação",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções não tratadas."""
    logger.error(f"❌ Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erro interno do servidor",
            "message": str(exc) if settings.DEBUG else "Erro interno"
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Verifica se a aplicação está rodando corretamente.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz.

    Retorna informações básicas da API.
    """
    return {
        "message": "Jornada do Empreendedor de Sucesso API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Inclui router da API v1
app.include_router(api_router, prefix="/api/v1")
