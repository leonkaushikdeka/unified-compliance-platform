from datetime import datetime, timedelta
from uuid import uuid4
import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import User
from src.models.assessment import (
    Framework,
    Assessment,
    ConsentRecord,
    DSRRequest,
    DataDiscoveryScan,
)
from src.services.auth import get_current_user
from src.schemas.dpdpa import (
    DataDiscoveryScanRequest,
    DataDiscoveryScanResponse,
    ConsentSessionCreate,
    ConsentSessionResponse,
    ConsentRequest,
    ConsentRecordResponse,
    DSRCreateRequest,
    DSRResponse,
    DSRProcessRequest,
    DPDPDashboardResponse,
)

logger = get_logger(__name__)
router = APIRouter()

PII_TYPES = [
    "PERSON_NAME",
    "PHONE_NUMBER",
    "EMAIL_ADDRESS",
    "AADHAAR_NUMBER",
    "PAN_NUMBER",
    "PASSPORT_NUMBER",
    "CREDIT_CARD_NUMBER",
    "BANK_ACCOUNT_NUMBER",
    "DATE_OF_BIRTH",
    "ADDRESS",
    "PIN_CODE",
]


def simulate_pii_scan(source_type: str):
    import random

    pii_found = []
    for pii_type in random.sample(PII_TYPES, k=random.randint(2, 6)):
        pii_found.append(
            {
                "type": pii_type,
                "count": random.randint(10, 10000),
                "risk_level": random.choice(["low", "medium", "high"]),
            }
        )
    risk_score = sum(
        {"low": 10, "medium": 30, "high": 50}[p["risk_level"]] for p in pii_found
    ) // max(len(pii_found), 1)
    return pii_found, risk_score


@router.post("/scan", response_model=DataDiscoveryScanResponse)
async def start_data_discovery_scan(
    scan_request: DataDiscoveryScanRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scan = DataDiscoveryScan(
        id=str(uuid4()),
        tenant_id=current_user.tenant_id,
        source_name=scan_request.source_name,
        source_type=scan_request.source_type,
        status="running",
        scan_config=scan_request.scan_config or {},
        created_by=current_user.id,
        started_at=datetime.utcnow(),
    )
    db.add(scan)
    await db.flush()

    pii_found, risk_score = simulate_pii_scan(scan_request.source_type)
    scan.pii_found = pii_found
    scan.risk_score = risk_score
    scan.status = "completed"
    scan.completed_at = datetime.utcnow()

    await db.flush()
    await db.refresh(scan)

    return DataDiscoveryScanResponse(
        id=scan.id,
        source_name=scan.source_name,
        source_type=scan.source_type,
        status=scan.status,
        pii_found=scan.pii_found,
        risk_score=scan.risk_score,
        data_flow=scan.data_flow,
        started_at=scan.started_at,
        completed_at=scan.completed_at,
    )


@router.get("/scans", response_model=list[DataDiscoveryScanResponse])
async def list_discovery_scans(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DataDiscoveryScan)
        .where(DataDiscoveryScan.tenant_id == current_user.tenant_id)
        .order_by(DataDiscoveryScan.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    scans = result.scalars().all()

    return [
        DataDiscoveryScanResponse(
            id=s.id,
            source_name=s.source_name,
            source_type=s.source_type,
            status=s.status,
            pii_found=s.pii_found,
            risk_score=s.risk_score,
            data_flow=s.data_flow,
            started_at=s.started_at,
            completed_at=s.completed_at,
        )
        for s in scans
    ]


@router.post("/consent/session", response_model=ConsentSessionResponse)
async def create_consent_session(
    session_data: ConsentSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session_id = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)

    consent_url = f"/consent/{session_id}?purpose={','.join(session_data.purposes)}"

    return ConsentSessionResponse(
        session_id=session_id,
        consent_url=consent_url,
        expires_at=expires_at,
    )


@router.post("/consent/record")
async def record_consent(
    consent_data: ConsentRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session_id = consent_data.session_id
    consent_proof = consent_data.proof or secrets.token_urlsafe(32)
    if consent_data.granted:
        consent_proof = hashlib.sha256(
            f"{session_id}:{consent_data.granted}:{consent_proof}".encode()
        ).hexdigest()

    record = ConsentRecord(
        id=str(uuid4()),
        tenant_id=current_user.tenant_id,
        data_subject_id="user@example.com",
        data_subject_type="email",
        purpose="general",
        consent_given=consent_data.granted,
        consent_proof=consent_proof,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(record)
    await db.commit()

    return {"message": "Consent recorded", "consent_proof": consent_proof}


@router.get("/consent", response_model=list[ConsentRecordResponse])
async def list_consent_records(
    data_subject_id: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(ConsentRecord).where(
        ConsentRecord.tenant_id == current_user.tenant_id,
    )
    if data_subject_id:
        query = query.where(ConsentRecord.data_subject_id == data_subject_id)

    result = await db.execute(
        query.order_by(ConsentRecord.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    records = result.scalars().all()

    return [
        ConsentRecordResponse(
            id=r.id,
            data_subject_id=r.data_subject_id,
            data_subject_type=r.data_subject_type,
            purpose=r.purpose,
            consent_given=r.consent_given,
            consent_proof=r.consent_proof,
            language=r.language,
            expires_at=r.expires_at,
            withdrawn_at=r.withdrawn_at,
            created_at=r.created_at,
        )
        for r in records
    ]


@router.post("/dsr", response_model=DSRResponse, status_code=201)
async def create_dsr_request(
    dsr_data: DSRCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    sla_due_date = datetime.utcnow() + timedelta(hours=72)

    dsr = DSRRequest(
        id=str(uuid4()),
        tenant_id=current_user.tenant_id,
        data_subject_id=dsr_data.data_subject_id,
        request_type=dsr_data.request_type,
        description=dsr_data.description,
        sla_due_date=sla_due_date,
        created_by=current_user.id,
    )
    db.add(dsr)
    await db.flush()
    await db.refresh(dsr)

    return DSRResponse(
        id=dsr.id,
        data_subject_id=dsr.data_subject_id,
        request_type=dsr.request_type,
        status=dsr.status,
        identity_verified=dsr.identity_verified,
        description=dsr.description,
        sla_due_date=dsr.sla_due_date,
        completed_at=dsr.completed_at,
        created_at=dsr.created_at,
    )


@router.get("/dsr", response_model=list[DSRResponse])
async def list_dsr_requests(
    status: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(DSRRequest).where(
        DSRRequest.tenant_id == current_user.tenant_id,
    )
    if status:
        query = query.where(DSRRequest.status == status)

    result = await db.execute(
        query.order_by(DSRRequest.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )
    dsrs = result.scalars().all()

    return [
        DSRResponse(
            id=d.id,
            data_subject_id=d.data_subject_id,
            request_type=d.request_type,
            status=d.status,
            identity_verified=d.identity_verified,
            description=d.description,
            sla_due_date=d.sla_due_date,
            completed_at=d.completed_at,
            created_at=d.created_at,
        )
        for d in dsrs
    ]


@router.get("/dsr/{dsr_id}", response_model=DSRResponse)
async def get_dsr_request(
    dsr_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DSRRequest).where(
            DSRRequest.id == dsr_id,
            DSRRequest.tenant_id == current_user.tenant_id,
        )
    )
    dsr = result.scalar_one_or_none()
    if not dsr:
        raise HTTPException(status_code=404, detail="DSR request not found")

    return DSRResponse(
        id=dsr.id,
        data_subject_id=dsr.data_subject_id,
        request_type=dsr.request_type,
        status=dsr.status,
        identity_verified=dsr.identity_verified,
        description=dsr.description,
        sla_due_date=dsr.sla_due_date,
        completed_at=dsr.completed_at,
        created_at=dsr.created_at,
    )


@router.post("/dsr/{dsr_id}/verify")
async def verify_dsr_identity(
    dsr_id: str,
    verification_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DSRRequest).where(
            DSRRequest.id == dsr_id,
            DSRRequest.tenant_id == current_user.tenant_id,
        )
    )
    dsr = result.scalar_one_or_none()
    if not dsr:
        raise HTTPException(status_code=404, detail="DSR request not found")

    dsr.identity_verified = True
    dsr.verification_method = verification_data.get("method", "email")
    await db.flush()

    return {"message": "Identity verified", "dsr_id": dsr_id}


@router.post("/dsr/{dsr_id}/process")
async def process_dsr_request(
    dsr_id: str,
    process_data: DSRProcessRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DSRRequest).where(
            DSRRequest.id == dsr_id,
            DSRRequest.tenant_id == current_user.tenant_id,
        )
    )
    dsr = result.scalar_one_or_none()
    if not dsr:
        raise HTTPException(status_code=404, detail="DSR request not found")

    if not dsr.identity_verified:
        raise HTTPException(status_code=400, detail="Identity not verified")

    dsr.status = "completed"
    dsr.completed_at = datetime.utcnow()
    dsr.notes = process_data.notes or ""
    await db.flush()

    return {"message": "DSR request processed", "dsr_id": dsr_id}


@router.get("/dashboard", response_model=DPDPDashboardResponse)
async def get_dpdashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scans_result = await db.execute(
        select(DataDiscoveryScan).where(
            DataDiscoveryScan.tenant_id == current_user.tenant_id,
        )
    )
    scans = scans_result.scalars().all()

    consent_result = await db.execute(
        select(ConsentRecord).where(
            ConsentRecord.tenant_id == current_user.tenant_id,
        )
    )
    consents = consent_result.scalars().all()

    dsr_result = await db.execute(
        select(DSRRequest).where(
            DSRRequest.tenant_id == current_user.tenant_id,
        )
    )
    dsrs = dsr_result.scalars().all()

    total_pii = sum(sum(p.get("count", 0) for p in s.pii_found or []) for s in scans)
    avg_risk = sum(s.risk_score for s in scans) / len(scans) if scans else 0
    consent_rate = len([c for c in consents if c.consent_given]) / max(len(consents), 1) * 100
    pending_dsrs = len([d for d in dsrs if d.status in ["pending", "in_progress"]])
    dsr_compliance = len([d for d in dsrs if d.status == "completed"]) / max(len(dsrs), 1) * 100

    return DPDPDashboardResponse(
        total_data_sources=len(scans),
        total_pii_records=total_pii,
        risk_score=int(avg_risk),
        consent_rate=round(consent_rate, 2),
        pending_dsrs=pending_dsrs,
        dsr_compliance_rate=round(dsr_compliance, 2),
        recent_scans=[
            DataDiscoveryScanResponse(
                id=s.id,
                source_name=s.source_name,
                source_type=s.source_type,
                status=s.status,
                pii_found=s.pii_found,
                risk_score=s.risk_score,
                data_flow=s.data_flow,
                started_at=s.started_at,
                completed_at=s.completed_at,
            )
            for s in scans[:5]
        ],
        consent_summary={
            "total": len(consents),
            "granted": len([c for c in consents if c.consent_given]),
            "withdrawn": len([c for c in consents if c.withdrawn_at]),
        },
    )
