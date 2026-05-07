from sqlalchemy.orm import Session

from fastapi import HTTPException

from app import (
    models,
    auth
)


def create_user(
    db: Session,
    data
):

    existing_email = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    existing_username = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = auth.hash_password(
        data.password
    )

    user = models.User(
        username=data.username,
        email=data.email,
        password=hashed_password,
        role="user"
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def login_user(
    db: Session,
    data
):

    user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not auth.verify_password(
        data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = auth.create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }