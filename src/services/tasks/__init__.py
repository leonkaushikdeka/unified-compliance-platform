from celery import shared_task


@shared_task(bind=True)
def cleanup_expired_sessions(self):
    return {"message": "Expired sessions cleanup completed", "count": 0}


@shared_task(bind=True)
def check_dsr_deadlines(self):
    return {"message": "DSR deadline check completed", "pending": 0}


@shared_task(bind=True)
def process_pii_scan(self, scan_id: str):
    return {"message": f"PII scan {scan_id} completed"}


@shared_task(bind=True)
def generate_compliance_report(self, report_id: str):
    return {"message": f"Report {report_id} generated"}
