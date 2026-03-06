from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerSettings:
    """Runtime configuration for Celery workers and persistence."""

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    result_backend_url: str = os.getenv("CELERY_RESULT_BACKEND", os.getenv("REDIS_URL", "redis://localhost:6379/1"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/landing_saas")
    kv_publish_endpoint: str | None = os.getenv("KV_PUBLISH_ENDPOINT")
    kv_publish_token: str | None = os.getenv("KV_PUBLISH_TOKEN")


SETTINGS = WorkerSettings()

COPY_GENERATION_QUEUE = "copy_generation"
PUBLISH_PIPELINE_QUEUE = "publish_pipeline"
ANALYTICS_PROCESSING_QUEUE = "analytics_processing"
