from sqlalchemy.orm import Session

from src.utils.bcrypt_password_manager import BcryptPasswordManager
from . import models, schemas


def create(request: schemas.TeacherCreate, db: Session):
    hashed_password = BcryptPasswordManager.hash_password(request.password)
    new_teacher = models.Teacher(email=request.email, password=hashed_password, first_name=request.first_name,
                                 last_name=request.last_name)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


def get_by_id(teacher_id: int, db: Session):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()


def get_by_email(email: str, db: Session):
    return db.query(models.Teacher).filter(models.Teacher.email == email).first()
