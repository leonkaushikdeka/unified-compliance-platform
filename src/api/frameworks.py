from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import Tenant, User
from src.models.assessment import Framework, Assessment
from src.services.auth import get_current_user
from src.schemas.framework import (
    FrameworkCreate,
    FrameworkResponse,
    FrameworkListResponse,
    AssessmentCreate,
    AssessmentResponse,
    AssessmentListResponse,
    DashboardMetrics,
)

logger = get_logger(__name__)
router = APIRouter()


@router.post("/frameworks", response_model=FrameworkResponse, status_code=201)
async def create_framework(
    framework_data: FrameworkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    framework = Framework(
        id=str(uuid4()),
        tenant_id=current_user.tenant_id,
        name=framework_data.name,
        description=framework_data.description,
        framework_type=framework_data.framework_type,
        controls=framework_data.controls,
        requirements=framework_data.requirements,
    )
    db.add(framework)
    await db.flush()
    await db.refresh(framework)
    return FrameworkResponse.from_orm(framework)


@router.get("/frameworks", response_model=FrameworkListResponse)
async def list_frameworks(
    framework_type: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Framework).where(
        Framework.tenant_id == current_user.tenant_id,
        Framework.is_active == True,
    )
    if framework_type:
        query = query.where(Framework.framework_type == framework_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    frameworks = result.scalars().all()

    return FrameworkListResponse(
        frameworks=[FrameworkResponse.from_orm(f) for f in frameworks],
        total=total,
    )


@router.get("/frameworks/{framework_id}", response_model=FrameworkResponse)
async def get_framework(
    framework_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Framework).where(
            Framework.id == framework_id,
            Framework.tenant_id == current_user.tenant_id,
        )
    )
    framework = result.scalar_one_or_none()
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return FrameworkResponse.from_orm(framework)


@router.post("/assessments", response_model=AssessmentResponse, status_code=201)
async def create_assessment(
    assessment_data: AssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Framework).where(
            Framework.id == assessment_data.framework_id,
            Framework.tenant_id == current_user.tenant_id,
        )
    )
    framework = result.scalar_one_or_none()
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")

    assessment = Assessment(
        id=str(uuid4()),
        tenant_id=current_user.tenant_id,
        framework_id=assessment_data.framework_id,
        name=assessment_data.name,
        description=assessment_data.description,
        due_date=assessment_data.due_date,
        status="draft",
        progress=0,
        score=0,
        created_by=current_user.id,
    )
    db.add(assessment)
    await db.flush()
    await db.refresh(assessment)
    return AssessmentResponse.from_orm(assessment)


@router.get("/assessments", response_model=AssessmentListResponse)
async def list_assessments(
    status: str = None,
    framework_id: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Assessment).where(
        Assessment.tenant_id == current_user.tenant_id,
    )
    if status:
        query = query.where(Assessment.status == status)
    if framework_id:
        query = query.where(Assessment.framework_id == framework_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    query = query.order_by(Assessment.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    assessments = result.scalars().all()

    return AssessmentListResponse(
        assessments=[AssessmentResponse.from_orm(a) for a in assessments],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
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
    return AssessmentResponse.from_orm(assessment)


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assessments_result = await db.execute(
        select(Assessment).where(
            Assessment.tenant_id == current_user.tenant_id,
        )
    )
    assessments = assessments_result.scalars().all()

    total = len(assessments)
    completed = len([a for a in assessments if a.status == "completed"])
    in_progress = len([a for a in assessments if a.status == "in_progress"])

    avg_score = sum(a.score for a in assessments) / total if total > 0 else 0
    compliance_rate = (completed / total * 100) if total > 0 else 0

    upcoming_deadlines = len(
        [
            a
            for a in assessments
            if a.due_date and a.due_date > datetime.utcnow() and a.status != "completed"
        ]
    )

    return DashboardMetrics(
        total_assessments=total,
        completed_assessments=completed,
        in_progress_assessments=in_progress,
        average_score=round(avg_score, 2),
        compliance_rate=round(compliance_rate, 2),
        upcoming_deadlines=upcoming_deadlines,
        recent_findings=[],
    )
