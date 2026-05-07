from passlib.context import CryptContext

from jose import (
    jwt,
    JWTError
)

from fastapi import (
    HTTPException,
    status
)

from datetime import (
    datetime,
    timedelta
)

from app.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        role = payload.get("role")

        if email is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return {
            "email": email,
            "role": role
        }

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )