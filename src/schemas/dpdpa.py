from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from src.models.assessment import ConsentRecord, DSRRequest, DataDiscoveryScan


class DataSourceCreate(BaseModel):
    source_name: str
    source_type: str
    connection_string: Optional[str] = None
    config: Optional[dict] = None


class DataSourceResponse(BaseModel):
    id: str
    source_name: str
    source_type: str
    status: str
    pii_found: Optional[List[dict]]
    risk_score: int
    created_at: datetime


class DataDiscoveryScanRequest(BaseModel):
    source_name: str
    source_type: str
    connection_string: Optional[str] = None
    scan_config: Optional[dict] = None


class DataDiscoveryScanResponse(BaseModel):
    id: str
    source_name: str
    source_type: str
    status: str
    pii_found: Optional[List[dict]]
    risk_score: int
    data_flow: Optional[dict]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


class ConsentSessionCreate(BaseModel):
    data_subject_identifier: str
    data_subject_type: str = "email"
    purposes: List[str]
    language: str = "en"
    expires_at: Optional[datetime] = None


class ConsentSessionResponse(BaseModel):
    session_id: str
    consent_url: str
    expires_at: datetime


class ConsentRecordResponse(BaseModel):
    id: str
    data_subject_id: str
    data_subject_type: str
    purpose: str
    consent_given: Optional[bool]
    consent_proof: Optional[str]
    language: str
    expires_at: Optional[datetime]
    withdrawn_at: Optional[datetime]
    created_at: datetime


class ConsentRequest(BaseModel):
    session_id: str
    granted: bool
    proof: Optional[str] = None


class DSRCreateRequest(BaseModel):
    data_subject_id: str
    request_type: str
    description: Optional[str] = None
    identity_verification: Optional[dict] = None


class DSRResponse(BaseModel):
    id: str
    data_subject_id: str
    request_type: str
    status: str
    identity_verified: bool
    description: Optional[str]
    sla_due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime


class DSRProcessRequest(BaseModel):
    data_sources: List[dict]
    notes: Optional[str] = None


class ComplianceReportRequest(BaseModel):
    report_type: str
    framework_id: Optional[str] = None
    assessment_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    format: str = "pdf"


class ComplianceReportResponse(BaseModel):
    report_id: str
    download_url: str
    expires_at: datetime


class DPDPDashboardResponse(BaseModel):
    total_data_sources: int
    total_pii_records: int
    risk_score: int
    consent_rate: float
    pending_dsrs: int
    dsr_compliance_rate: float
    recent_scans: List[DataDiscoveryScanResponse]
    consent_summary: dict
