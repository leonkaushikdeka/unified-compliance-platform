from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship

from src.core.database import Base


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    version = Column(String(20), default="1.0")
    description = Column(Text)
    framework_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    controls = Column(JSON, default=list)
    requirements = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="frameworks")
    assessments = relationship("Assessment", back_populates="framework")

    def __repr__(self):
        return f"<Framework(id={self.id}, name={self.name}, type={self.framework_type})>"


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    framework_id = Column(String(36), ForeignKey("frameworks.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="draft")
    progress = Column(Integer, default=0)
    score = Column(Integer, default=0)
    findings = Column(JSON, default=list)
    evidence = Column(JSON, default=dict)
    controls_status = Column(JSON, default=dict)
    metadata = Column(JSON, default=dict)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    due_date = Column(DateTime)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="assessments")
    framework = relationship("Framework", back_populates="assessments")
    dsr_requests = relationship(
        "DSRRequest", back_populates="assessment", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Assessment(id={self.id}, name={self.name}, status={self.status})>"


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    data_subject_id = Column(String(255), nullable=False)
    data_subject_type = Column(String(50), default="email")
    purpose = Column(String(255), nullable=False)
    consent_given = Column(Boolean)
    consent_proof = Column(Text)
    language = Column(String(10), default="en")
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    expires_at = Column(DateTime)
    withdrawn_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<ConsentRecord(id={self.id}, purpose={self.purpose}, consent={self.consent_given})>"
        )


class DSRRequest(Base):
    __tablename__ = "dsr_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    assessment_id = Column(String(36), ForeignKey("assessments.id"), nullable=True)
    data_subject_id = Column(String(255), nullable=False)
    request_type = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    identity_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))
    description = Column(Text)
    notes = Column(Text, default="[]")
    sla_due_date = Column(DateTime)
    completed_at = Column(DateTime)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship("Tenant")
    assessment = relationship("Assessment", back_populates="dsr_requests")

    def __repr__(self):
        return f"<DSRRequest(id={self.id}, type={self.request_type}, status={self.status})>"


class DataDiscoveryScan(Base):
    __tablename__ = "data_discovery_scans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    source_name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    pii_found = Column(JSON, default=list)
    risk_score = Column(Integer, default=0)
    data_flow = Column(JSON, default=dict)
    scan_config = Column(JSON, default=dict)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DataDiscoveryScan(id={self.id}, source={self.source_name}, status={self.status})>"
