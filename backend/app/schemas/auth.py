"""
Schemas para autenticação.
"""
from pydantic import BaseModel, EmailStr
from app.schemas.user import UserPublic


class UserLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """Schema para registro de novo usuário."""
    email: EmailStr
    password: str
    full_name: str


class Token(BaseModel):
    """Schema para resposta de token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenResponse(Token):
    """Schema para resposta de token com dados do usuário."""
    user: UserPublic


class RefreshRequest(BaseModel):
    """Schema para requisição de refresh token."""
    refresh_token: str


class TokenPayload(BaseModel):
    """Schema para payload do token."""
    sub: str  # user_id
    exp: int
    type: str  # access ou refresh
