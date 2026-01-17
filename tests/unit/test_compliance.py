import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from datetime import datetime
from uuid import uuid4


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        from src.services.auth import hash_password

        password = "test_password_123"
        hashed = hash_password(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_verify_password_correct(self):
        from src.services.auth import hash_password, verify_password

        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        from src.services.auth import hash_password, verify_password

        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False

    def test_hash_password_unique(self):
        from src.services.auth import hash_password

        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2


class TestTokenGeneration:
    def test_create_access_token(self):
        from src.services.auth import create_access_token, decode_token

        data = {"sub": "user123", "email": "test@example.com"}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

        payload = decode_token(token)
        assert payload is not None
        assert payload.sub == "user123"
        assert payload.email == "test@example.com"
        assert payload.type == "access"

    def test_create_refresh_token(self):
        from src.services.auth import create_refresh_token, decode_token

        data = {"sub": "user123"}
        token = create_refresh_token(data)
        assert isinstance(token, str)

        payload = decode_token(token)
        assert payload is not None
        assert payload.sub == "user123"
        assert payload.type == "refresh"

    def test_decode_token_invalid(self):
        from src.services.auth import decode_token

        result = decode_token("invalid_token")
        assert result is None


class TestFrameworkControls:
    def test_soc2_controls_structure(self):
        from src.services.frameworks.soc2 import get_soc2_controls

        controls = get_soc2_controls()
        assert len(controls) > 0
        for control_id, control in controls.items():
            assert "name" in control
            assert "description" in control
            assert "category" in control

    def test_gdpr_controls_structure(self):
        from src.services.frameworks.gdpr import get_gdpr_controls

        controls = get_gdpr_controls()
        assert len(controls) > 0
        for control_id, control in controls.items():
            assert "name" in control
            assert "description" in control
            assert "article" in control

    def test_assess_soc2_control(self):
        from src.services.frameworks.soc2 import assess_soc2_control

        evidence = {
            "policy_exists": True,
            "procedure_documented": True,
            "training_completed": True,
        }
        result = assess_soc2_control("CC1.1", evidence)
        assert result["score"] > 0
        assert result["status"] in ["compliant", "partial", "non_compliant"]

    def test_assess_gdpr_control(self):
        from src.services.frameworks.gdpr import assess_gdpr_control

        evidence = {
            "policy_documented": True,
            "process_implemented": True,
        }
        result = assess_gdpr_control("ART5.1.A", evidence)
        assert result["score"] > 0
        assert result["status"] in ["compliant", "partial", "non_compliant"]


class TestModels:
    def test_tenant_model(self):
        from src.models.user import Tenant

        tenant = Tenant(
            id=str(uuid4()),
            name="Test Company",
            slug="test-company",
        )
        assert tenant.name == "Test Company"
        assert tenant.slug == "test-company"
        assert tenant.is_active is True

    def test_user_model(self):
        from src.models.user import User

        user = User(
            id=str(uuid4()),
            tenant_id=str(uuid4()),
            email="test@example.com",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe",
        )
        assert user.email == "test@example.com"
        assert user.full_name == "John Doe"
        assert user.is_active is True


class TestSchemas:
    def test_login_request_schema(self):
        from src.schemas.auth import LoginRequest

        data = LoginRequest(email="test@example.com", password="password123")
        assert data.email == "test@example.com"
        assert data.password == "password123"

    def test_framework_response_schema(self):
        from src.schemas.framework import FrameworkResponse

        response = FrameworkResponse(
            id=str(uuid4()),
            name="SOC2",
            description="SOC2 Compliance",
            framework_type="SOC2",
            version="1.0",
            is_active=True,
            controls=[],
            requirements=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        assert response.name == "SOC2"
        assert response.is_active is True
