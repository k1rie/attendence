from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.apps.auth.dependecies import get_current_user
from src.apps.classrooms import service as classroom_service
from src.apps.students import service as student_service
from src.apps.teachers.models import Teacher
from src.database.session import get_db
from src.utils.cloudinary_uploader import CloudinaryUploader
from src.utils.report_generator import ReportGenerator
from . import service as attendance_service
from .schemas import Attendance, GenerateReportResponse

router = APIRouter(
    prefix="/attendances",
    tags=["attendances"],
    responses={404: {"description": "Not found"}},
)


@router.post("/classrooms/{classroom_id}/students/{student_id}", status_code=201, response_model=Attendance)
def create(classroom_id: int, student_id: int, current_user: Teacher = Depends(get_current_user),
           db: Session = Depends(get_db)):
    classroom = classroom_service.get_by_id(classroom_id, db)

    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    if classroom.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the teacher of this classroom")

    student = student_service.get_by_id(student_id, db)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.classroom_id != classroom_id:
        raise HTTPException(status_code=403, detail="Student does not belong to this classroom")

    # check if attendance already exists from today
    attendance = attendance_service.get_by_classroom_id_and_student_id_and_date(classroom_id, student_id, db)

    if attendance is None:
        attendance = attendance_service.create(classroom_id, student_id, db)

    return attendance


@router.get("/classrooms/{classroom_id}/start_date/{start_date}/end_date/{end_date}",
            response_model=GenerateReportResponse)
def generate_report(classroom_id: int, start_date: str, end_date: str,
                    current_user: Teacher = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    classroom = classroom_service.get_by_id(classroom_id, db)

    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    if classroom.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the teacher of this classroom")

    attendances = attendance_service.get_list_by_classroom_id_and_date_range(classroom_id, start_date, end_date, db)

    file_path = ReportGenerator.generate_excel_attendance(attendances)

    url = CloudinaryUploader.upload_file(file_path)

    return {"url": url}
