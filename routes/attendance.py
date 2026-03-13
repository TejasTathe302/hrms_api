from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from database import get_db
from models import Attendance, Employee
from schemas import AttendanceCreate, AttendanceResponse

router = APIRouter()


@router.post("/attendance", response_model=AttendanceResponse, status_code=201)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    # Check if employee exists
    prev_attendance = db.query(Attendance).filter(Attendance.employee_id == attendance.employee_id, Attendance.date == attendance.date).first()
    if prev_attendance:
        raise HTTPException(status_code=404, detail="Attendance already marked")

    db_attendance = Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status,
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)

    return AttendanceResponse(
        id=db_attendance.id,
        employee_id=db_attendance.employee_id,
        date=db_attendance.date,
        status=db_attendance.status,
    )


@router.get("/attendance/{employee_id}", response_model=list[AttendanceResponse])
def get_attendance(
    employee_id: int,
    date_filter: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    query = db.query(Attendance).filter(Attendance.employee_id == employee_id)

    if date_filter:
        query = query.filter(Attendance.date == date_filter)

    records = query.order_by(Attendance.date.desc()).all()

    return [
        AttendanceResponse(
            id=r.id,
            employee_id=r.employee_id,
            date=r.date,
            status=r.status,
            employee_name=employee.full_name,
        )
        for r in records
    ]


@router.get("/attendance", response_model=list[AttendanceResponse])
def get_all_attendance(
    date_filter: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    query = db.query(Attendance).join(Employee)

    if date_filter:
        query = query.filter(Attendance.date == date_filter)

    records = query.order_by(Attendance.date.desc()).all()

    return [
        AttendanceResponse(
            id=r.id,
            employee_id=r.employee_id,
            date=r.date,
            status=r.status,
            employee_name=r.employee.full_name,
        )
        for r in records
    ]
