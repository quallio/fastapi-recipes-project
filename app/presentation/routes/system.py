from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
def healthcheck():
    return {"status": "ok"}

@router.get("/version", tags=["System"])
def version():
    return {"version": "0.1.0"}
