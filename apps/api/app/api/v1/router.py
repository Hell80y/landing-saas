from fastapi import APIRouter

router = APIRouter()


@router.get("/status", tags=["status"])
def status() -> dict[str, str]:
    return {"service": "api", "status": "ready"}


api_router = APIRouter()
api_router.include_router(router)
