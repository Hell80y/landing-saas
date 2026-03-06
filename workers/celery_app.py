from __future__ import annotations

from celery import Celery
from kombu import Exchange, Queue

from workers.config import (
    ANALYTICS_PROCESSING_QUEUE,
    COPY_GENERATION_QUEUE,
    PUBLISH_PIPELINE_QUEUE,
    SETTINGS,
)

celery_app = Celery(
    "landing_workers",
    broker=SETTINGS.redis_url,
    backend=SETTINGS.result_backend_url,
    include=["workers.tasks"],
)

celery_app.conf.update(
    task_default_exchange="landing_workers",
    task_default_exchange_type="direct",
    task_default_routing_key=COPY_GENERATION_QUEUE,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_queues=(
        Queue(COPY_GENERATION_QUEUE, Exchange("landing_workers"), routing_key=COPY_GENERATION_QUEUE),
        Queue(PUBLISH_PIPELINE_QUEUE, Exchange("landing_workers"), routing_key=PUBLISH_PIPELINE_QUEUE),
        Queue(ANALYTICS_PROCESSING_QUEUE, Exchange("landing_workers"), routing_key=ANALYTICS_PROCESSING_QUEUE),
    ),
    task_routes={
        "workers.tasks.generate_copy_spec": {"queue": COPY_GENERATION_QUEUE, "routing_key": COPY_GENERATION_QUEUE},
        "workers.tasks.assemble_combined_spec": {"queue": PUBLISH_PIPELINE_QUEUE, "routing_key": PUBLISH_PIPELINE_QUEUE},
        "workers.tasks.publish_to_kv": {"queue": PUBLISH_PIPELINE_QUEUE, "routing_key": PUBLISH_PIPELINE_QUEUE},
    },
)
