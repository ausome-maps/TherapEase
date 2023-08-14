from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from models.users import UserResponse, CreateUserSchema, UserBaseSchema
from libs.users.crud import create_user, retrieve_user


router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def register_user(payload: CreateUserSchema):
    new_user = create_user(payload)
    if not new_user[0]:
        if new_user[1] == "Account already exists":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=new_user[1]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=new_user[1]
            )

    return {"status": "success", "user": new_user[1]}


# @router.get("/users/protected", response_model=UserResponse)
# async def read_users_me(
#     current_user: Annotated[UserBaseSchema, Depends(get_current_active_user)]
# ):
#     return {"status": "success", "user": current_user}
