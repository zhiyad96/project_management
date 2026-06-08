from sqlalchemy.orm import Session
from fastapi import Response,Depends

from models.user import customuser
from service.users import get_user_by_email
from datetime import datetime, timedelta
from jose import jwt,JWTError
from config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS
from service.security import verify_password
from fastapi import Cookie, HTTPException
from database.database import get_db





def authenticate_user(db: Session,email: str,password: str):
    user = get_user_by_email(db,email)
    if not user:
        return None
    if not verify_password(password,user.password):
        return None
    return user



def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = (datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)



def create_refresh_token(data: dict):
    payload = data.copy()
    payload["exp"] = (datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)



def get_current_user(db: Session = Depends(get_db),access_token: str = Cookie(None)):
    print("accesstoken ", access_token)
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload["sub"])

        user = (
            db.query(customuser)
            .filter(customuser.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
        

def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")