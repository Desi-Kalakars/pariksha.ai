from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping_pong():
    return {"message": "pong"}
