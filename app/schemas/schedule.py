"""Pydantic models for schedule data — stub for future implementation."""

from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class Shift(BaseModel):
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    shift_code: str = ""
    employee_id: str = ""


class Schedule(BaseModel):
    id: str
    week_start: date
    shifts: list[Shift] = []
