from datetime import datetime
from uuid import uuid4
import json
import io
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.models.assessment import Assessment, Framework
from src.services.auth import get_current_user
from src.schemas.dpdpa import ComplianceReportRequest, ComplianceReportResponse

logger = get_logger(__name__)
router = APIRouter()


@router.post("/generate", response_model=ComplianceReportResponse)
async def generate_report(
    report_data: ComplianceReportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    report_id = str(uuid4())
    expires_at = datetime.utcnow()

    if report_data.format == "pdf":
        expires_at = expires_at
    else:
        expires_at = expires_at

    return ComplianceReportResponse(
        report_id=report_id,
        download_url=f"/api/v1/reports/download/{report_id}",
        expires_at=expires_at,
    )


@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessments = result.scalars().all()

    report_data = {
        "report_id": report_id,
        "generated_at": datetime.utcnow().isoformat(),
        "tenant_id": current_user.tenant_id,
        "summary": {
            "total_assessments": len(assessments),
            "completed": len([a for a in assessments if a.status == "completed"]),
            "in_progress": len([a for a in assessments if a.status == "in_progress"]),
            "average_score": sum(a.score for a in assessments) / max(len(assessments), 1),
        },
        "assessments": [
            {
                "name": a.name,
                "status": a.status,
                "score": a.score,
                "progress": a.progress,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            }
            for a in assessments
        ],
    }

    output = io.StringIO()
    json.dump(report_data, output, indent=2)
    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=compliance_report_{report_id}.json"},
    )


@router.get("/templates")
async def list_report_templates(
    current_user: User = Depends(get_current_user),
):
    return [
        {
            "id": "executive_summary",
            "name": "Executive Summary",
            "description": "High-level compliance overview",
        },
        {
            "id": "detailed_assessment",
            "name": "Detailed Assessment",
            "description": "Full assessment report with findings",
        },
        {
            "id": "gap_analysis",
            "name": "Gap Analysis",
            "description": "Control gaps and remediation priorities",
        },
        {
            "id": "sla_compliance",
            "name": "SLA Compliance",
            "description": "DSR and compliance deadline tracking",
        },
    ]
