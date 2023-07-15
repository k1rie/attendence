from sqlalchemy.orm import Session

from . import schemas, models


def create(request: schemas.StudentCreate, db: Session):
    new_student = models.Student(**request.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def get_by_id(student_id: int, db: Session):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_by_email(email: str, db: Session):
    return db.query(models.Student).filter(models.Student.email == email).first()


def get_by_classroom_id(classroom_id: int, db: Session):
    return db.query(models.Student).filter(models.Student.classroom_id == classroom_id).all()
