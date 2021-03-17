from fastapi import APIRouter, Depends
from api.auth import schemas, crud
from api.user.models import Users
from api.utils.db_utils import database
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()
@router.get("/users/email",response_model = schemas.UserList)
async def find_user_by_email(email : str):
    query = Users.__table__.select().where(Users.email== email)
    return await database.fetch_one(query)

@router.get("/users/username", response_model= schemas.UserList)
async def find_user_by_username(username : str):
    query = Users.__table__.select().where(Users.username == username)
    return await database.fetch_one(query)

@router.delete("/users/username")
async def delete_user_by_username(username: str):
    query = Users.__table__.delete().where(Users.username == username)
    await database.execute(query)
    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }

@router.get("/users/{userId}", response_model=schemas.UserList)
async def find_user_by_id(userId: str):
    query = Users.__table__.select().where(Users.id == userId)
    return await database.fetch_one(query)
    
@router.delete("/users/{userId}")
async def delete_user(user : schemas.UserDelete):
    query = Users.__table__.delete().where(Users.id == user.id)
    await database.execute(query=query)

    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }


@router.get("/users",response_model=Page[schemas.UserList],dependencies=[Depends(pagination_params)])
async def find_all_user(
    currentuser : schemas.UserList = Depends(crud.get_current_active_user),
):
    query = "select * from Users"
    user_all = await database.fetch_all(query=query, values={}) 
    return paginate(user_all)
