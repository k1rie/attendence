from datetime import date

from pydantic import BaseModel


class AttendanceBase(BaseModel):
    date: date
    attended: bool


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: int
    student_id: int
    classroom_id: int

    class Config:
        orm_mode = True


class GenerateReportResponse(BaseModel):
    url: str
