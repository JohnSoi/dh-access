from datetime import timedelta, datetime, UTC

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from dh_access.consts import TokenType
from dh_access.settings import access_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_token(data: dict, expires_delta: timedelta | None = None, token_type: TokenType = TokenType.ACCESS) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=access_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, access_settings.SECRET_APP, algorithm=access_settings.ALGORITHM)

    return encoded_jwt