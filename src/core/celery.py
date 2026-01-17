import os
from celery import Celery

from src.core.config import settings

os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

celery_app = Celery(
    "compliance-platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_URL,
    include=[
        "src.services.tasks.dpdpa",
        "src.services.tasks.reports",
        "src.services.tasks.notifications",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=60 * 60 * 24,
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "src.services.tasks.cleanup_expired_sessions",
            "schedule": 60 * 60,
        },
        "check-dsr-deadlines": {
            "task": "src.services.tasks.check_dsr_deadlines",
            "schedule": 60 * 60,
        },
    },
)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    pass


def get_celery_app() -> Celery:
    return celery_app
