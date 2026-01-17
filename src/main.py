from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.logging import get_logger
from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.dpdpa import router as dpdpa_router
from src.api.frameworks import router as frameworks_router
from src.api.assessments import router as assessments_router
from src.api.reports import router as reports_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Compliance Platform", env=settings.APP_ENV)
    yield
    logger.info("Shutting down Compliance Platform")


app = FastAPI(
    title="Compliance Platform API",
    description="Unified compliance platform for DPDP, SOC2, GDPR, HIPAA, ISO27001, NIST, CMMC",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

if settings.APP_ENV == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.CORS_ORIGINS,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/api/metrics")

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(dpdpa_router, prefix="/api/v1/dpdpa")
app.include_router(frameworks_router, prefix="/api/v1/frameworks")
app.include_router(assessments_router, prefix="/api/v1/assessments")
app.include_router(reports_router, prefix="/api/v1/reports")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
    }
