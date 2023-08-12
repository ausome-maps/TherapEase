from fastapi import APIRouter, Request, Response, Security, HTTPException, status
from fastapi_jwt import JwtAuthorizationCredentials
from dependencies import access_security, refresh_security
from datetime import timedelta
from libs.users.crud import retrieve_user
from libs.encrypt import verify_password
from models.users import LoginUserSchema, UserResponse

router = APIRouter()


@router.post("/login")
def auth(payload: LoginUserSchema):
    user = retrieve_user(payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )
    subject = {"email": user["email"], "role": "user"}
    return {
        "access_token": access_security.create_access_token(subject=subject),
        "refresh_token": access_security.create_refresh_token(subject=subject),
    }


@router.post("/auth_cookie")
def auth(response: Response):
    subject = {"username": "username", "role": "user"}
    access_token = access_security.create_access_token(subject=subject)
    access_security.set_access_cookie(response, access_token)
    return {"access_token": access_token}


@router.post("/refresh")
def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(
        subject=credentials.subject, expires_delta=timedelta(days=2)
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
