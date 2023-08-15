from typing import Optional, Union, Dict, Any
from passlib.context import CryptContext
from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin

from fastapi_users import BaseUserManager, InvalidPasswordException
from fastapi_users.password import PasswordHelper

from models.users import User, UserCreate, get_user_db
import dependencies

SECRET = dependencies.SECRET_KEY

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)


# Create a UserManager that can be used in tests. This is the constructor
class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Called after a user has registered. This is a no - op for now

        @param user - The user that has registered.
        @param request - The request that triggered the event. If the event is a request for a user this should be the request
        """
        print(f"User {user.id} has registered.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        Called after a user has verified their email. This is a no - op for requests that don't require verification.

        @param user - The user that has verified the email. It's assumed that the user is logged in
        @param token - The token sent by the user
        @param request - The request
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Validate password. This is a method to be overridden by sub - classes.

        @param password - The password to be validated. Must be at least 8 characters long and not contain e - mail
        @param user - The user that is being validated

        @return True if
        """
        # Raises InvalidPasswordException if password is too long
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        # Raise InvalidPasswordException if user. email is not in password
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        """
        Called after a user has been updated. By default nothing happens.
        Subclasses can override this to do anything you want to be done after the update is done

        @param user - The user that has been updated
        @param update_dict - The dictionary containing the changes to be made
        @param request - The request that triggered
        """
        print(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        Called after a user forgets their password. This is a no - op for now

        @param user - The user who forgets their password.
        @param token - The token returned by : meth : ` get_token `.
        @param request - The request that triggered the event. If ` ` None ` ` the event wasn't triggered
        """
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ):
        """
        Called after a user resets their password. This is a no - op for now

        @param user - The user who reset their password.
        @param request - The request being responded to if any. Not used
        """
        print(f"User {user.id} has reset their password.")

    async def on_before_delete(self, user: User, request: Optional[Request] = None):
        """
        Called before a user is deleted. By default prints a message to the console.

        @param user - The user that is going to be deleted.
        @param request - The request that triggered the event. Not used
        """
        print(f"User {user.id} is going to be deleted")

    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        """
        Called after a user is deleted. This is a no - op for now

        @param user - The user that is being deleted
        @param request - The request that was
        """
        print(f"User {user.id} is successfully deleted")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    """
    Get a UserManager for use in tests.
    This is a context manager that can be used to interact with the user database without having to worry about user authentication.

    @param user_db - User database to use for authentication. If not provided it will be guessed
    """
    yield UserManager(user_db, password_helper)
