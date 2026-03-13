"""
Schemas Pydantic para validação e serialização de dados.
"""
from app.schemas.auth import UserLogin, UserRegister, Token, TokenPayload
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserInDB, UserPublic
from app.schemas.assessment import (
    AssessmentBase,
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentInDB,
    AssessmentPublic,
)
from app.schemas.response import (
    ResponseBase,
    ResponseCreate,
    ResponseInDB,
    ResponsePublic,
)
from app.schemas.result import (
    DISCScores,
    SpiralScores,
    PAEIScores,
    EnneagramScores,
    ValoresScores,
    ArquetiposScores,
    ResultComplete,
    ResultPublic,
)
from app.schemas.report import (
    ReportBase,
    ReportCreate,
    ReportInDB,
    ReportPublic,
)

__all__ = [
    # Auth
    "UserLogin",
    "UserRegister",
    "Token",
    "TokenPayload",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserPublic",
    # Assessment
    "AssessmentBase",
    "AssessmentCreate",
    "AssessmentUpdate",
    "AssessmentInDB",
    "AssessmentPublic",
    # Response
    "ResponseBase",
    "ResponseCreate",
    "ResponseInDB",
    "ResponsePublic",
    # Result
    "DISCScores",
    "SpiralScores",
    "PAEIScores",
    "EnneagramScores",
    "ValoresScores",
    "ArquetiposScores",
    "ResultComplete",
    "ResultPublic",
    # Report
    "ReportBase",
    "ReportCreate",
    "ReportInDB",
    "ReportPublic",
]
