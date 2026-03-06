from fastapi import FastAPI

from apps.api.database import create_db_and_tables
from apps.api.routers.landings import router as landings_router
from apps.api.routers.payments import router as payments_router

app = FastAPI(title="Landing SaaS API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(landings_router)
app.include_router(payments_router)
