from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.apps.auth.dependecies import get_current_user
from src.apps.teachers.schemas import Teacher
from src.database.session import get_db
from . import service
from .schemas import ClassroomCreate, Classroom

router = APIRouter(
    prefix="/classrooms",
    tags=["classrooms"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Classroom, status_code=201)
def create(classroom: ClassroomCreate, current_user: Teacher = Depends(get_current_user),
           db: Session = Depends(get_db)):
    classroom = service.create(classroom, current_user.id, db)
    return classroom


@router.get("/", response_model=list[Classroom])
def get_all(current_user: Teacher = Depends(get_current_user), db: Session = Depends(get_db)):
    classrooms = service.get_list_by_teacher_id(current_user.id, db)
    return classrooms


@router.get("/{classroom_id}", response_model=Classroom)
def get(classroom_id: int, current_user: Teacher = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = service.get_by_id(classroom_id, db)

    if teacher is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    classroom = service.get_by_id(classroom_id, db)

    if classroom.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to access this classroom")

    return classroom
