"""Schedule API routes — stub for future implementation."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_schedules():
    return {"schedules": []}


@router.get("/{schedule_id}")
async def get_schedule(schedule_id: str):
    return {"schedule_id": schedule_id, "data": None}
