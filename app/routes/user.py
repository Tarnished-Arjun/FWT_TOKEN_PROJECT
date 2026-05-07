from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app import (
    schemas,
    crud,
    auth
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


security = HTTPBearer()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    credentials = Depends(security)
):

    token = credentials.credentials

    return auth.verify_token(token)

def admin_only(
    current_user = Depends(get_current_user)
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


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


@router.get("/profile")
def profile(
    current_user = Depends(get_current_user)
):

    return {
        "message": "Authorized Access",
        "user": current_user
    }


@router.get("/admin")
def admin_dashboard(
    current_user = Depends(admin_only)
):

    return {
        "message": "Welcome Admin",
        "user": current_user
    }