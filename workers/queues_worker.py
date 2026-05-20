from celery import Celery

from app.config.config import get_settings


settings = get_settings()


celery_app = Celery(
    "password_security_workers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


# Global Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "workers.breach_checker.*": {"queue": "breach_queue"},
    },
)


# Auto-discover tasks inside workers package
celery_app.autodiscover_tasks(["workers"])        

if __name__ == "__main__":
    celery_app.start()
