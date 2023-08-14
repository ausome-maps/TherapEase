from fastapi import APIRouter, Request, Response, Security, HTTPException, status
from fastapi_jwt import JwtAuthorizationCredentials
from dependencies import access_security, refresh_security
from datetime import timedelta
from libs.auth import authenticate_user, retrieve_user, create_access_token
from models.users import LoginUserSchema, UserResponse

router = APIRouter()


@router.post("/login")
def auth(payload: LoginUserSchema):
    user = retrieve_user(payload.email)
    user = authenticate_user(user["email"], payload.password)
    if user is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    # subject = {"email": user["email"], "role": "user"}
    # return {
    #     "access_token": access_security.create_access_token(subject=subject),
    #     "refresh_token": access_security.create_refresh_token(subject=subject),
    # }

 
@router.post("/refresh")
def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(
        subject=credentials.subject, expires_delta=timedelta(days=2)
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
