from fastapi import APIRouter, Depends, HTTPException, UploadFile , File
from . import crud, schemas
from api.user.models import Users
import uuid, datetime
from api.utils.db_utils import database
from api.utils import constant
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.user import models
from api.utils.db_utils import engine
from api.user.controller import find_user_by_username
from . import py_controller
from api.user.controller import find_email_by_username
import cloudinary
import cloudinary.uploader
router = APIRouter()

models.Base.metadata.create_all(bind=engine)
@router.post("/auth/register/")
async def register_user(user : schemas.UserCreate):
    result = await crud.find_existed_user(user.email)
    if result:
        raise HTTPException(status_code=404, detail="User Already Existed")
    
    gid = str(uuid.uuid1())
    gdate = datetime.datetime.now()
    query = Users.__table__.insert().values(
        id = gid,
        username = user.username,
        email = user.email,
        password = crud.get_password_hash(user.password),
        firstname = user.firstname,
        lastname = user.lastname,
        phone = user.phone,
        created_at = gdate,
        url = user.url,
        status = "1",
        passcode = '0')
    await database.execute(query)
    py_controller.generate_register_email([user.email])
    return {
        **user.dict(),
        "id" :gid,
        "created_at" : gdate,
        "status" : "1",
        "passcode" : "0",
    }
    

@router.post("/auth/login", response_model = schemas.Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()):

    userDB = await crud.find_existed_user(form_data.username) #(username)
    print("this is username" ,form_data.username)
    if not userDB:
        raise HTTPException(status_code = 404, detail="User Not Found")

    user = schemas.UserPWD(**userDB)
    isValid = crud.verify_password(form_data.password, user.password) #(password)
    print("This is password", form_data.password)
    if not isValid:
        raise HTTPException(status_code = 404, detail="Incorrect Username Or Password")
    # query = " Select email From users where username='"+str(form_data.username)+"'"
    # result = await database.fetch_one(query)
    # print(result)
    # print(form_data.username)
    #return result["email"]
    access_token_expires = crud.timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data ={"sub": form_data.username},
        expires_delta= access_token_expires,
    )

    results = {
        "access_token": access_token,
        "token_type": "bearer",
        "expired_in" : constant.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "user_info" : user
    }
    print(user.email)
    py_controller.generate_login_email([user.email])
    return results

@router.put("/auth/update",response_model=schemas.UserList)
async def update_user(user : schemas.UserUpdate):
    gDate = datetime.datetime.now()
    query = Users.__table__.update().\
        where(Users.username == user.username).\
            values(
                firstname = user.firstname,
                lastname = user.lastname,
                phone = user.phone,
                created_at = gDate
            )
    await database.execute(query)
    #return {"status" : True}
    return await find_user_by_username(user.username)

@router.put("/auth/upload")
async def upload_profile_picture(username : str, file: UploadFile = File(...)):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    query = Users.__table__.update().\
        where(Users.username == username).\
            values( url = url)
    await database.execute(query)
    #return {"status" : True}
    return await find_user_by_username(username)

@router.put("/auth/change_password", response_model=schemas.UserList)
async def change_password(user : schemas.UserChange):
    query = Users.__table__.update().\
        where(Users.username == user.username).\
            values(
                password =crud.get_password_hash(user.new_password),
               # confirm_password = util.get_password_hash(user.confirm_password)
            )
    await database.execute(query)
    #return {"message" : "Password Change Succesfully"}
    return await find_user_by_username(user.username)

from api.auth.crud import get_current_user
@router.post("/login/test-token", response_model=schemas.UserList)
def test_token(current_user: schemas.UserInDB = Depends(get_current_user)):
    """
    Test access token.
    """
    return current_user

@router.post('/auth')
async def get_user_auth(email: str):
    #check = util.findExistedEmailUser(database=database,email=email)
    check = py_controller.check_user_exist(email,engine)
    if check:
        passcode1 = await py_controller.send_auth_code(email)
        py_controller.generate_auth_email(passcode1,[email])
        return {"status":'Sent Passcode'}
    else:
        return  {"message":"Check your email-id"}

@router.post('/forget')
async def forget(email: str,passcode:int,new_pass:str):
    validate=py_controller.validate_passcode(email,passcode,engine)
    if validate:
        passcode = await py_controller.update_password(email,new_pass)
        py_controller.generate_password_change_email([email])
        return {"status":'Success'}
    else:
        return {"status":"Passcode is wrong"}