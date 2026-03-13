"""
Schemas Pydantic para User (Usuário).
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Schema base de usuário."""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)


class UserCreate(UserBase):
    """Schema para criação de usuário."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema para atualização de usuário (todos campos opcionais)."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema de usuário como armazenado no banco (com hash de senha)."""
    id: UUID
    password_hash: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """Schema de usuário para resposta pública (sem password_hash)."""
    id: UUID
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True
