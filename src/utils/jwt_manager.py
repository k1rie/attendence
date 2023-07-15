from datetime import datetime, timedelta
from typing import Union, Any

from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "sdfdsfasdfasd!2kjlj"  # os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = "kljlkjlkj!kjlj#jlk"  # os.environ['JWT_REFRESH_SECRET_KEY']


class JWTManager:

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is None:
            expires_delta = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        else:
            expires_delta = datetime.utcnow() + expires_delta

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is None:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = datetime.utcnow() + expires_delta

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt
