
---

## Conținut recomandat AGENTS.md

```md
# AGENTS.md

This file defines implementation rules for AI coding agents working in this repository.

Agents must follow these guidelines when modifying the codebase.

---

# Architecture Rules

This repository is a monorepo containing:

apps/web → Next.js dashboard  
apps/api → FastAPI backend  
workers → Celery background jobs  
cloudflare → landing runtime worker  

---

# Code Quality Rules

All code must:

- be modular
- follow clear folder structure
- avoid unnecessary dependencies
- include typing where possible
- follow best practices for security

---

# Frontend Rules

Framework:
Next.js + React + TailwindCSS

Design system uses:

design tokens via CSS variables

Blocks architecture:

Hero  
Benefits  
SocialProof  
Pricing  
FAQ  
FinalCTA

Themes must be composed using blocks.

No duplicated layouts.

---

# Backend Rules

Framework:
FastAPI

Use:

Pydantic models  
SQLAlchemy or SQLModel  
Alembic migrations  

All endpoints must validate input.

---

# Worker Rules

Celery must be used for background tasks.

Queues include:

copy_generation  
publish_pipeline  
analytics_processing  

Workers must be idempotent.

---

# Cloudflare Worker Rules

Landing runtime must:

read CombinedSpec from KV  
avoid database calls  
cache responses  

Edge response target:

< 50ms.

---

# Security Rules

Validate Stripe webhooks.

Never expose secrets.

Use environment variables.

---

# Review Checklist

Agents must verify:

project builds successfully  
API endpoints start correctly  
Cloudflare worker compiles  
database migrations run  
no runtime errors

---

# Development Principle

Prefer simple and scalable architecture.

Avoid over-engineering.
