from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.models.assessment import Assessment, Framework
from src.services.auth import get_current_user
from src.schemas.framework import (
    AssessmentUpdate,
    AssessmentResponse,
    AssessmentSubmitControls,
    ControlStatus,
)

logger = get_logger(__name__)
router = APIRouter()


@router.put("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def update_assessment(
    assessment_id: str,
    update_data: AssessmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if update_data.name is not None:
        assessment.name = update_data.name
    if update_data.description is not None:
        assessment.description = update_data.description
    if update_data.due_date is not None:
        assessment.due_date = update_data.due_date
    if update_data.status is not None:
        assessment.status = update_data.status

    await db.flush()
    await db.refresh(assessment)
    return AssessmentResponse.from_orm(assessment)


@router.post("/assessments/{assessment_id}/start")
async def start_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.status != "draft":
        raise HTTPException(status_code=400, detail="Assessment already started")

    assessment.status = "in_progress"
    assessment.started_at = datetime.utcnow()
    await db.flush()

    return {"message": "Assessment started", "assessment_id": assessment_id}


@router.post("/assessments/{assessment_id}/controls", response_model=AssessmentResponse)
async def submit_control_status(
    assessment_id: str,
    controls_data: AssessmentSubmitControls,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    current_controls = assessment.controls_status or {}
    for control in controls_data.controls:
        current_controls[control.control_id] = {
            "status": control.status,
            "evidence": control.evidence,
            "notes": control.notes,
        }

    assessment.controls_status = current_controls
    total_controls = len(current_controls)
    completed_controls = len(
        [c for c in current_controls.values() if c.get("status") == "compliant"]
    )
    assessment.progress = int(
        (completed_controls / total_controls * 100) if total_controls > 0 else 0
    )

    await db.flush()
    await db.refresh(assessment)
    return AssessmentResponse.from_orm(assessment)


@router.post("/assessments/{assessment_id}/complete", response_model=AssessmentResponse)
async def complete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if assessment.status != "in_progress":
        raise HTTPException(status_code=400, detail="Assessment not in progress")

    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()

    controls = assessment.controls_status or {}
    total = len(controls)
    compliant = len([c for c in controls.values() if c.get("status") == "compliant"])
    assessment.score = int((compliant / total * 100) if total > 0 else 0)

    findings = []
    for control_id, control_data in controls.items():
        if control_data.get("status") == "non_compliant":
            findings.append(
                {
                    "control_id": control_id,
                    "issue": f"Control {control_id} is non-compliant",
                    "severity": "high",
                }
            )
    assessment.findings = findings

    await db.flush()
    await db.refresh(assessment)
    return AssessmentResponse.from_orm(assessment)


@router.delete("/assessments/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    await db.delete(assessment)
    await db.commit()

    return {"message": "Assessment deleted"}
