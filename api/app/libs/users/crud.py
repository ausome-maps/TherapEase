from datetime import datetime, timedelta
from bson.objectid import ObjectId

# from app import oauth2
from database import User
from libs import auth
from serializers.user_serializers import userEntity, userResponseEntity


def create_user(payload):
    user = User.find_one({"email": payload.email.lower()})
    if user:
        return False, "Account already exists"
    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        return False, "Password do not match"
    #  Hash the password
    payload.password = auth.get_hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = "user"
    payload.disabled = False
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = userResponseEntity(User.find_one({"_id": result.inserted_id}))
    return True, new_user


def retrieve_user(email: str):
    db_user = User.find_one({"email": email.lower()})
    if not db_user:
        return False
    user = userEntity(db_user)
    return user
