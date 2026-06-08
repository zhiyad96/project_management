from sqlalchemy.orm import Session
from models.user import customuser
from schemas.user import UserCreate, UserUpdate
from service.security import hash_password




def create_user(db: Session, user_data: UserCreate):
    hashed = hash_password(user_data.password)
    new_user = customuser(
        name     = user_data.name,
        email    = user_data.email,
        password = hashed,
        role     = user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(customuser).offset(skip).limit(limit).all()



def get_user_by_id(db: Session, user_id: int):
    return db.query(customuser).filter(customuser.id == user_id).first()



def get_user_by_email(db: Session, email: str):
    return db.query(customuser).filter(customuser.email == email).first()



def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in user_data.model_dump(exclude_unset=True).items():
        if key == "password" and value:
            value = hash_password(value)
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user



def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user