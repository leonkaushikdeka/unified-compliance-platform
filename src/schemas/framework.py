from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from src.models.assessment import Framework, Assessment


class FrameworkCreate(BaseModel):
    name: str
    description: Optional[str] = None
    framework_type: str
    controls: Optional[List[dict]] = None
    requirements: Optional[List[dict]] = None


class FrameworkResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    framework_type: str
    version: str
    is_active: bool
    controls: Optional[List[dict]]
    requirements: Optional[List[dict]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj: Framework) -> "FrameworkResponse":
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            framework_type=obj.framework_type,
            version=obj.version,
            is_active=obj.is_active,
            controls=obj.controls,
            requirements=obj.requirements,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class FrameworkListResponse(BaseModel):
    frameworks: List[FrameworkResponse]
    total: int


class AssessmentCreate(BaseModel):
    framework_id: str
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class AssessmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class ControlStatus(BaseModel):
    control_id: str
    status: str
    evidence: Optional[List[str]] = None
    notes: Optional[str] = None


class AssessmentSubmitControls(BaseModel):
    controls: List[ControlStatus]


class AssessmentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    progress: int
    score: int
    findings: Optional[List[dict]]
    controls_status: Optional[dict]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    framework: Optional[FrameworkResponse] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj: Assessment) -> "AssessmentResponse":
        framework = None
        if obj.framework:
            framework = FrameworkResponse.from_orm(obj.framework)
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            status=obj.status,
            progress=obj.progress,
            score=obj.score,
            findings=obj.findings,
            controls_status=obj.controls_status,
            started_at=obj.started_at,
            completed_at=obj.completed_at,
            due_date=obj.due_date,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            framework=framework,
        )


class AssessmentListResponse(BaseModel):
    assessments: List[AssessmentResponse]
    total: int
    page: int
    page_size: int


class DashboardMetrics(BaseModel):
    total_assessments: int
    completed_assessments: int
    in_progress_assessments: int
    average_score: float
    compliance_rate: float
    upcoming_deadlines: int
    recent_findings: List[dict]
