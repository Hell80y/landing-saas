# Workers

Celery background workers for landing generation and publishing.

## Queues

- `copy_generation`
- `publish_pipeline`
- `analytics_processing`

## Tasks

- `generate_copy_spec`
- `assemble_combined_spec`
- `publish_to_kv`

## Run

```bash
celery -A workers.celery_app:celery_app worker -Q copy_generation,publish_pipeline,analytics_processing --loglevel=info
```

## Environment

- `REDIS_URL` (broker)
- `CELERY_RESULT_BACKEND` (optional, defaults to Redis)
- `DATABASE_URL`
- `KV_PUBLISH_ENDPOINT` (optional)
- `KV_PUBLISH_TOKEN` (optional)
