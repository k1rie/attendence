from sqlalchemy.orm import Session

from . import models, schemas


def create(request: schemas.ClassroomCreate, teacher_id: int, db: Session):
    new_classroom = models.Classroom(name=request.name, teacher_id=teacher_id)
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return new_classroom


def get_by_id(classroom_id: int, db: Session):
    return db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()


def get_list_by_teacher_id(teacher_id: int, db: Session):
    return db.query(models.Classroom).filter(models.Classroom.teacher_id == teacher_id).all()
