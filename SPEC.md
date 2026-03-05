# Landing SaaS – Technical Specification

## Goal
Build a SaaS platform that automatically generates high-conversion landing pages for digital or physical products.

The system should:
- generate landing pages using AI
- allow editing via a dashboard
- publish static runtime pages served via Cloudflare Workers
- integrate Stripe for payments
- support multi-tenant SaaS accounts

---

# Domain Architecture

app.domain.com → Dashboard (Next.js / Vercel)

api.domain.com → Backend API (FastAPI / Fly or Render)

l.domain.com → Landing runtime (Cloudflare Workers)

assets.domain.com → Static assets (Cloudflare R2)

t.domain.com → Event tracking collector (Cloudflare Worker)

---

# Core Stack

Frontend:
Next.js + React + TailwindCSS

Backend:
FastAPI (Python)

Workers:
Celery + Redis

Database:
Postgres

Cache:
Redis

Landing Runtime:
Cloudflare Worker + KV

Payments:
Stripe + Stripe Connect

---

# Core Entities

users  
tenants  
landings  
landing_versions  
subscriptions  
events  
jobs  
connect_accounts

---

# Landing Architecture

Landing pages are generated from a CombinedSpec JSON object.

CombinedSpec contains:

- design tokens
- content (copy + assets)
- page structure
- commerce configuration
- tracking configuration

---

# CombinedSpec Example Structure

```json
{
  "meta": {},
  "design": {},
  "content": {},
  "page": {},
  "commerce": {},
  "tracking": {}
}
