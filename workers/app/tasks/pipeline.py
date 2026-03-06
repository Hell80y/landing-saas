from app.celery_app import celery_app


@celery_app.task(name="tasks.noop", bind=True)
def noop(self: object) -> dict[str, str]:
    """Idempotent placeholder task for pipeline wiring validation."""

    return {"status": "queued"}
