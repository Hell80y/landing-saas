from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import Settings

settings = Settings()

app = FastAPI(title="Landing SaaS API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "environment": settings.api_env}
