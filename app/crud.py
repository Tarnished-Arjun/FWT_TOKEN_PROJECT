from app import models, auth

def create_user(db, data):
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

    return user