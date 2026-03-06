from celery import Celery

celery_app = Celery("landing_workers")
celery_app.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
    task_default_queue="copy_generation",
    task_queues=(
        {"name": "copy_generation"},
        {"name": "publish_pipeline"},
        {"name": "analytics_processing"},
    ),
)

celery_app.autodiscover_tasks(["app.tasks"])
