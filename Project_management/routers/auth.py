from fastapi import (APIRouter,Depends,HTTPException,Response,status,Cookie)
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.auth import LoginRequest
from service.auth import authenticate_user,get_current_user,logout_user
from service.auth import (create_access_token,create_refresh_token)

router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/login")
def login(credentials: LoginRequest,response: Response,db: Session = Depends(get_db)):

    user = authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id)
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,      
        samesite="none",
        max_age=1800       
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,      
        samesite="none",
        max_age=604800     
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role":user.role
        }
    }
    
    
@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }
    
    

@router.post("/logout")
def logout(response: Response, current_user=Depends(get_current_user)):
    logout_user(response)
    return {"message": "Logged out successfully"}



from jose import jwt, JWTError
from config import (
    SECRET_KEY,
    ALGORITHM
)

@router.post("/refresh")
def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None)):
    print("reffresh token ",refresh_token)
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print(payload)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        access_token = create_access_token(
            {
                "sub": user_id
            }
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="none",
            max_age=1800
        )

        return {
            "message": "Token refreshed"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )