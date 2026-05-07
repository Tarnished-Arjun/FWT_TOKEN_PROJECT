from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app import (
    schemas,
    crud
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/signup",
    response_model=schemas.UserResponse
)
def signup(
    data: schemas.UserSignup,
    db: Session = Depends(get_db)
):

    return crud.create_user(
        db,
        data
    )


@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    data: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    return crud.login_user(
        db,
        data
    )