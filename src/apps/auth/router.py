from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.apps.teachers import service as teacher_service
from src.database.session import get_db
from src.utils.bcrypt_password_manager import BcryptPasswordManager
from src.utils.jwt_manager import JWTManager
from .schemas import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/accesses",
    tags=["accesses"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=LoginResponse, status_code=201)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    teacher = teacher_service.get_by_email(request.email, db)

    if teacher is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    is_password_correct = BcryptPasswordManager.check_password(request.password, teacher.password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = JWTManager.create_access_token(teacher.email)

    return {"token": access_token}
