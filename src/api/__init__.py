from src.api.auth import router as auth_router
from src.api.health import router as health_router
from src.api.dpdpa import router as dpdpa_router
from src.api.frameworks import router as frameworks_router
from src.api.assessments import router as assessments_router
from src.api.reports import router as reports_router

__all__ = [
    "auth_router",
    "health_router",
    "dpdpa_router",
    "frameworks_router",
    "assessments_router",
    "reports_router",
]
