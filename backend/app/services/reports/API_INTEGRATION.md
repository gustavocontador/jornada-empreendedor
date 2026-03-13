# INTEGRAÇÃO COM A API - ENGINE DE RELATÓRIOS

Guia completo para integrar a engine de relatórios com endpoints FastAPI.

## 📡 Endpoints Recomendados

### 1. POST /api/v1/reports/simplified

Gera relatório simplificado (2-3 páginas)

**Request:**
```json
{
  "result_id": "uuid-do-resultado",
  "user_id": "uuid-do-usuario"
}
```

**Response (Success):**
```json
{
  "success": true,
  "report_type": "simplified",
  "pdf_path": "/tmp/reports/relatorio_simplificado_<user_id>_<timestamp>.pdf",
  "file_size_bytes": 245678,
  "generated_at": "2024-03-13T00:54:23.456Z",
  "download_url": "/api/v1/reports/download/<report_id>"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Result not found",
  "detail": "Result with id <uuid> does not exist"
}
```

---

### 2. POST /api/v1/reports/complete

Gera relatório completo (15-20 páginas)

**Request:**
```json
{
  "result_id": "uuid-do-resultado",
  "user_id": "uuid-do-usuario"
}
```

**Response (Success):**
```json
{
  "success": true,
  "report_type": "complete",
  "pdf_path": "/tmp/reports/relatorio_completo_<user_id>_<timestamp>.pdf",
  "file_size_bytes": 1567890,
  "pages": 18,
  "generated_at": "2024-03-13T00:54:23.456Z",
  "download_url": "/api/v1/reports/download/<report_id>"
}
```

---

### 3. GET /api/v1/reports/download/{report_id}

Download do PDF gerado

**Response:**
- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="relatorio_<timestamp>.pdf"`
- Binary PDF data

---

### 4. GET /api/v1/reports/list/{user_id}

Lista todos os relatórios de um usuário

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "report_id": "uuid",
      "type": "complete",
      "generated_at": "2024-03-13T00:54:23.456Z",
      "file_size_bytes": 1567890,
      "download_url": "/api/v1/reports/download/<report_id>"
    },
    {
      "report_id": "uuid",
      "type": "simplified",
      "generated_at": "2024-03-12T15:30:12.123Z",
      "file_size_bytes": 245678,
      "download_url": "/api/v1/reports/download/<report_id>"
    }
  ]
}
```

---

### 5. DELETE /api/v1/reports/{report_id}

Deleta um relatório

**Response:**
```json
{
  "success": true,
  "message": "Report deleted successfully"
}
```

---

## 🔧 Implementação dos Endpoints

### Arquivo: `app/api/v1/endpoints/reports.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path

from app.db.session import get_db
from app.models.user import User
from app.models.result import Result
from app.models.report import Report
from app.services.reports import ReportGenerator
from app.api import deps
from app.schemas.report import (
    ReportGenerateRequest,
    ReportGenerateResponse,
    ReportListResponse
)

router = APIRouter()


@router.post("/simplified", response_model=ReportGenerateResponse)
async def generate_simplified_report(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    request_data: ReportGenerateRequest
):
    """
    Gera relatório simplificado (2-3 páginas).
    """
    # Validar que o resultado existe e pertence ao usuário
    result = db.query(Result).filter(
        Result.id == request_data.result_id,
        Result.user_id == current_user.id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found or does not belong to user"
        )

    # Gerar relatório
    try:
        generator = ReportGenerator(db)
        pdf_path = generator.generate_simplified_report(
            result_id=str(request_data.result_id),
            user_id=str(current_user.id)
        )

        # Salvar registro no banco
        report = Report(
            user_id=current_user.id,
            result_id=result.id,
            type="simplified",
            file_path=pdf_path,
            file_size=os.path.getsize(pdf_path)
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        return ReportGenerateResponse(
            success=True,
            report_type="simplified",
            report_id=report.id,
            pdf_path=pdf_path,
            file_size_bytes=report.file_size,
            download_url=f"/api/v1/reports/download/{report.id}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )


@router.post("/complete", response_model=ReportGenerateResponse)
async def generate_complete_report(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    request_data: ReportGenerateRequest
):
    """
    Gera relatório completo (15-20 páginas).
    """
    # Validar que o resultado existe e pertence ao usuário
    result = db.query(Result).filter(
        Result.id == request_data.result_id,
        Result.user_id == current_user.id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found or does not belong to user"
        )

    # Gerar relatório
    try:
        generator = ReportGenerator(db)
        pdf_path = generator.generate_complete_report(
            result_id=str(request_data.result_id),
            user_id=str(current_user.id)
        )

        # Salvar registro no banco
        report = Report(
            user_id=current_user.id,
            result_id=result.id,
            type="complete",
            file_path=pdf_path,
            file_size=os.path.getsize(pdf_path)
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        return ReportGenerateResponse(
            success=True,
            report_type="complete",
            report_id=report.id,
            pdf_path=pdf_path,
            file_size_bytes=report.file_size,
            download_url=f"/api/v1/reports/download/{report.id}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Faz download de um relatório gerado.
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found on disk"
        )

    filename = Path(report.file_path).name
    return FileResponse(
        path=report.file_path,
        media_type="application/pdf",
        filename=filename
    )


@router.get("/list", response_model=ReportListResponse)
async def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista todos os relatórios do usuário atual.
    """
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).order_by(Report.created_at.desc()).all()

    return ReportListResponse(
        success=True,
        reports=reports
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Deleta um relatório.
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Deletar arquivo físico
    if os.path.exists(report.file_path):
        os.remove(report.file_path)

    # Deletar registro do banco
    db.delete(report)
    db.commit()

    return {"success": True, "message": "Report deleted successfully"}
```

---

## 📦 Schemas Necessários

### Arquivo: `app/schemas/report.py`

```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid


class ReportGenerateRequest(BaseModel):
    """Request para geração de relatório."""
    result_id: uuid.UUID
    user_id: uuid.UUID


class ReportGenerateResponse(BaseModel):
    """Response de geração de relatório."""
    success: bool
    report_type: str  # "simplified" ou "complete"
    report_id: uuid.UUID
    pdf_path: str
    file_size_bytes: int
    download_url: str
    generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportItemResponse(BaseModel):
    """Informações de um relatório na listagem."""
    report_id: uuid.UUID
    type: str
    generated_at: datetime
    file_size_bytes: int
    download_url: str

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    """Response de listagem de relatórios."""
    success: bool
    reports: List[ReportItemResponse]
```

---

## 🗄️ Modelo do Banco de Dados

### Arquivo: `app/models/report.py`

```python
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Report(Base):
    """Modelo de relatório gerado."""
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    result_id = Column(UUID(as_uuid=True), ForeignKey("results.id", ondelete="CASCADE"), nullable=False, index=True)

    type = Column(String, nullable=False)  # "simplified" ou "complete"
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # em bytes

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports")
    result = relationship("Result", back_populates="reports")

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, type={self.type}, user_id={self.user_id})>"
```

---

## 🔐 Autenticação e Permissões

Certifique-se de:

1. **Apenas o dono pode gerar/baixar/deletar seus relatórios**
2. **Validar que o `result_id` pertence ao usuário**
3. **Rate limiting** para evitar abuse (max 10 relatórios/hora por exemplo)

---

## 🚀 Registro dos Endpoints

### Arquivo: `app/api/v1/api.py`

```python
from fastapi import APIRouter

from app.api.v1.endpoints import users, assessments, reports

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])  # NOVO
```

---

## 🧪 Testando os Endpoints

### 1. Gerar relatório simplificado

```bash
curl -X POST "http://localhost:8000/api/v1/reports/simplified" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "result_id": "uuid-do-resultado",
    "user_id": "uuid-do-usuario"
  }'
```

### 2. Baixar relatório

```bash
curl -X GET "http://localhost:8000/api/v1/reports/download/<report-id>" \
  -H "Authorization: Bearer <token>" \
  --output relatorio.pdf
```

### 3. Listar relatórios

```bash
curl -X GET "http://localhost:8000/api/v1/reports/list" \
  -H "Authorization: Bearer <token>"
```

---

## 📊 Monitoramento e Logs

Adicione logs em pontos-chave:

```python
import logging

logger = logging.getLogger(__name__)

# No início da geração
logger.info(f"Generating {report_type} report for user {user_id}")

# Após sucesso
logger.info(f"Report generated successfully: {pdf_path} ({file_size} bytes)")

# Em caso de erro
logger.error(f"Error generating report: {str(e)}", exc_info=True)
```

---

## 🎯 Performance e Otimizações

1. **Geração assíncrona:** Para relatórios completos (mais lentos), considere:
   ```python
   from fastapi import BackgroundTasks

   @router.post("/complete/async")
   async def generate_complete_report_async(
       background_tasks: BackgroundTasks,
       ...
   ):
       background_tasks.add_task(generate_report_task, result_id, user_id)
       return {"message": "Report generation started", "job_id": job_id}
   ```

2. **Cache:** Cache relatórios já gerados se o `result` não mudou

3. **CDN:** Para produção, considere upload para S3/CloudFront

---

## ✅ Checklist de Implementação

- [ ] Criar modelo `Report` no banco
- [ ] Criar schemas `ReportGenerateRequest`, `ReportGenerateResponse`
- [ ] Implementar endpoints em `app/api/v1/endpoints/reports.py`
- [ ] Registrar router em `app/api/v1/api.py`
- [ ] Adicionar testes unitários
- [ ] Adicionar testes de integração
- [ ] Configurar rate limiting
- [ ] Adicionar logging
- [ ] Documentar no Swagger/OpenAPI
- [ ] Testar com dados reais

---

## 📞 Próximos Passos

Após implementar os endpoints:

1. **Frontend:** Criar botões "Gerar Relatório" na UI
2. **Notificações:** Email com link de download quando relatório estiver pronto
3. **Analytics:** Track quantos relatórios são gerados (métricas de uso)
4. **Monetização:** Relatório simplificado grátis, completo pago?

---

## 🎉 Conclusão

A engine está 100% pronta. Agora basta:
1. Implementar os endpoints seguindo este guia
2. Testar com dados reais
3. Ajustar textos/interpretações conforme necessário
4. Deploy!
