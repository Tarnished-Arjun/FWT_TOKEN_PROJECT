from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas, auth

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


@router.post("/signup")
def signup(
    data: schemas.UserSignup,
    db: Session = Depends(get_db)
):
    hashed_password = auth.hash_password(
        data.password
    )

    user = models.User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "User registered successfully"
    }