"""Pydantic models for staff data — stub for future implementation."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class StaffMember(BaseModel):
    id: str
    name: str
    department: Optional[str] = None
    email: Optional[EmailStr] = None
