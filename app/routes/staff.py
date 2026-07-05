"""Staff API routes — stub for future implementation."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_staff():
    return {"staff": []}


@router.get("/{staff_id}")
async def get_staff(staff_id: str):
    return {"staff_id": staff_id, "data": None}
