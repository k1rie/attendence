from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError

from src.apps.teachers import service as teacher_service
from src.apps.teachers.schemas import Teacher
from src.database.session import get_db
from src.utils.jwt_manager import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from .schemas import TokenPayload

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/accesses/login",
    scheme_name="JWT",
)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.token_payload = None

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return self.token_payload
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            self.token_payload = TokenPayload(**payload)
        except(jwt.JWTError, ValidationError):
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


token_bearer = JWTBearer()


def get_current_user(token_payload: TokenPayload = Depends(token_bearer), db=Depends(get_db)):
    teacher: Teacher = teacher_service.get_by_email(token_payload.sub, db)

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return teacher
