from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
import re


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department: str

    @field_validator("employee_id")
    @classmethod
    def employee_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Employee ID is required")
        return v.strip()

    @field_validator("full_name")
    @classmethod
    def full_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Full name is required")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if not v or not v.strip():
            raise ValueError("Email is required")
        v = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("department")
    @classmethod
    def department_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Department is required")
        return v.strip()


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: str

    @field_validator("status")
    @classmethod
    def status_valid(cls, v):
        if v not in ("Present", "Absent"):
            raise ValueError("Status must be 'Present' or 'Absent'")
        return v


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    status: str
    employee_name: Optional[str] = None

    class Config:
        from_attributes = True
