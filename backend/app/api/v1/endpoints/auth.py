"""
Endpoints de autenticação.

Gerencia registro, login, refresh de token e informações do usuário logado.
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.db.session import get_db
from app.models.user import User
from app.schemas import auth as auth_schema
from app.schemas import user as user_schema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Dependency: obtém usuário atual a partir do JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Verifica tipo do token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency: verifica se usuário está ativo."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    return current_user


def get_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency: verifica se usuário é admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões insuficientes. Apenas administradores."
        )
    return current_user


@router.post("/register", response_model=auth_schema.TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: user_schema.UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Registra novo usuário no sistema.

    Retorna tokens de acesso e refresh.
    """
    # Verifica se email já existe
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Cria novo usuário
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password),
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Gera tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/login", response_model=auth_schema.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Login OAuth2 compatível.

    Retorna tokens de acesso e refresh.
    """
    # Busca usuário por email
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verifica credenciais
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica se está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    # Gera tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/refresh", response_model=auth_schema.TokenResponse)
def refresh(
    refresh_data: auth_schema.RefreshRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Renova access token usando refresh token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(refresh_data.refresh_token)
    if payload is None:
        raise credentials_exception

    # Verifica tipo do token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception

    # Gera novos tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=user_schema.UserPublic)
def get_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna dados do usuário logado.
    """
    return current_user
