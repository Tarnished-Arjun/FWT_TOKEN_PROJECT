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

@router.post("/login")
def login(
    data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    if not auth.verify_password(
        data.password,
        user.password
    ):
        return {
            "message": "Invalid password"
        }

    access_token = auth.create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }