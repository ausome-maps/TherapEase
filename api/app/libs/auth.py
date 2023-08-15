import dependencies
from beanie import PydanticObjectId
from fastapi_users.authentication import (
    JWTStrategy,
    BearerTransport,
    AuthenticationBackend,
)
from fastapi_users import FastAPIUsers
from libs.users.user_manager import get_user_manager
from models.users import User


def get_jwt_strategy() -> JWTStrategy:
    """
    Create a JWTStrategy for use with JWT. It is recommended to use : func : ` get_jwt ` instead of this function.


    @return A JWTStrategy with secret and lifetime_seconds set to 3600 seconds ( default ). Example :. from twisted. python import
    """
    return JWTStrategy(
        secret=dependencies.SECRET_KEY,
        lifetime_seconds=dependencies.ACCESS_TOKEN_EXPIRES_IN,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)