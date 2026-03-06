# Landing SaaS Monorepo

Scaffold for a multi-service Landing SaaS platform.

## Monorepo Structure

- `apps/web` — Next.js dashboard (TailwindCSS, block-based UI)
- `apps/api` — FastAPI backend (Pydantic, SQLModel/Alembic-ready)
- `workers` — Celery background jobs
- `cloudflare/landing` — Cloudflare Worker runtime for landing pages
- `cloudflare/tracking` — Cloudflare Worker for tracking/event collection
- `infra` — environment/deployment templates (`docker`, `fly`, `render`)

## Prerequisites

- Docker + Docker Compose
- Node.js 20+
- Python 3.11+

## Local Infrastructure (Postgres + Redis)

```bash
docker compose -f docker-compose.dev.yml up -d
```

## Service Setup (Scaffold Stage)

Copy environment templates before starting services:

```bash
cp .env.example .env
cp apps/web/.env.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env
cp workers/.env.example workers/.env
cp cloudflare/landing/.env.example cloudflare/landing/.dev.vars
cp cloudflare/tracking/.env.example cloudflare/tracking/.dev.vars
```

At this stage, the repository only includes project scaffolding and base configuration.
