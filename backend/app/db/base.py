"""
SQLAlchemy Base e imports de modelos.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User  # noqa
from app.models.assessment import Assessment  # noqa
from app.models.question import Question  # noqa
from app.models.response import Response  # noqa
from app.models.result import Result  # noqa
from app.models.report import Report  # noqa
