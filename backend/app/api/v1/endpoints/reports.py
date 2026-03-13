"""
Endpoints de reports (relatórios em PDF).

Gerencia geração e download de relatórios.
"""
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.models.result import Result
from app.models.report import Report
from app.schemas import report as report_schema

router = APIRouter()


@router.post("/generate", response_model=report_schema.ReportPublic, status_code=status.HTTP_201_CREATED)
def generate_report(
    report_in: report_schema.ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Gera relatório PDF a partir de um assessment.

    Tipos disponíveis:
    - simplified: Relatório resumido (5-10 páginas)
    - complete: Relatório completo (30-40 páginas)
    """
    # Verifica se assessment existe e pertence ao usuário
    assessment = db.query(Assessment).filter(
        Assessment.id == report_in.assessment_id
    ).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment não encontrado"
        )

    if assessment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para gerar relatório deste assessment"
        )

    # Verifica se assessment foi completado
    if assessment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment ainda não foi finalizado"
        )

    # Verifica se resultado existe
    result = db.query(Result).filter(
        Result.assessment_id == report_in.assessment_id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultados não encontrados. Execute POST /assessments/{id}/complete primeiro."
        )

    # Valida tipo de relatório
    if report_in.report_type not in ["simplified", "complete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de relatório inválido. Use 'simplified' ou 'complete'."
        )

    # TODO: Aqui você implementaria a geração real do PDF
    # Por enquanto, vamos criar apenas o registro com status "pending"
    # A geração real pode ser feita de forma assíncrona usando Celery ou similar

    # Verifica se já existe relatório deste tipo
    existing_report = db.query(Report).filter(
        Report.assessment_id == report_in.assessment_id,
        Report.report_type == report_in.report_type
    ).first()

    if existing_report:
        # Retorna relatório existente
        return existing_report

    # Cria novo relatório
    report = Report(
        user_id=current_user.id,
        assessment_id=report_in.assessment_id,
        report_type=report_in.report_type,
        status="pending",  # Pode ser: pending, generating, completed, failed
        file_path=None,  # Será preenchido quando PDF for gerado
        metadata=report_in.metadata or {}
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # TODO: Disparar task assíncrona para gerar PDF
    # exemplo: generate_pdf_task.delay(report.id)

    return report


@router.get("/{report_id}", response_model=report_schema.ReportPublic)
def get_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retorna metadados do relatório.

    Não retorna o PDF, apenas informações sobre o relatório.
    """
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )

    if report.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este relatório"
        )

    return report


@router.get("/{report_id}/download")
def download_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> FileResponse:
    """
    Faz download do arquivo PDF do relatório.

    Retorna erro 404 se relatório ainda não foi gerado.
    """
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado"
        )

    if report.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este relatório"
        )

    # Verifica se relatório foi gerado
    if report.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Relatório ainda não está pronto. Status atual: {report.status}"
        )

    if not report.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo do relatório não encontrado"
        )

    # TODO: Verificar se arquivo existe no sistema de arquivos
    # import os
    # if not os.path.exists(report.file_path):
    #     raise HTTPException(status_code=404, detail="Arquivo não existe")

    # Retorna arquivo para download
    filename = f"relatorio_{report.report_type}_{report_id}.pdf"

    return FileResponse(
        path=report.file_path,
        media_type="application/pdf",
        filename=filename
    )
