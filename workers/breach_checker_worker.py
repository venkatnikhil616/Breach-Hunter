from typing import Dict, Optional
                                                  from celery import Celery

from app.config.config import get_settings
from app.services.breach_service import check_breach                                                

settings = get_settings()

celery_app = Celery(
    "breach_checker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)                                                 
# Optional Celery configuration                   celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(name="workers.breach_checker.check_password_breach", bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def check_password_breach(self, password: str) -> Dict[str, Optional[int]]:
    """
    Celery task to check if a password has been breached.
    Returns:
    {
        "breached": bool,
        "breach_count": int | None
    }
    """
    # Run async function from sync context
    import asyncio                                
    return asyncio.run(check_breach(password))
