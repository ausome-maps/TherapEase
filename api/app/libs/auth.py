from typing import Annotated
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.users import UserBaseSchema
from libs.users.crud import retrieve_user
import dependencies

ACCESS_TOKEN_EXPIRES_IN = dependencies.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = dependencies.REFRESH_TOKEN_EXPIRES_IN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(email: str, password: str):
    user = retrieve_user(email)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, dependencies.SECRET_KEY, algorithms=[dependencies.JWT_ALGORITHM]
        )
        print(payload.get("sub"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = retrieve_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserBaseSchema, Depends(get_current_user)]
):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, dependencies.SECRET_KEY, algorithm=dependencies.JWT_ALGORITHM
    )
    return encoded_jwt
