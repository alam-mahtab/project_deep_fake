from pydantic import BaseModel, Field
from typing import Optional
import datetime
class UserCreate(BaseModel):
    username : str
    email    : str
    phone    : str
    password : str
    firstname: str
    lastname : str
    url      : Optional[str]
class UserList(BaseModel):
    id : str
    username : str
    email : str
    firstname : str
    lastname : str
    phone : str
    created_at : Optional[datetime.datetime]
    status: str
    
class UserUpdate(BaseModel):
    username : str = Field(..., example="Enter Your username")
    email : str 
    username : str
    firstname : str
    lastname : str
    phone : str
class Token(BaseModel):
    access_token : str
    token_type : str
    expired_in : str
    user_info : UserList

class TokenData(BaseModel):
    username : str =None

class UserPWD(UserList):
    password : str
class UserChange(BaseModel):
    username : str = Field(..., example="Enter Your username")
    new_password : str
class UserInDB(UserList):
    salt: str = ""
    hashed_password: str = ""

class UserDelete(BaseModel):
    id : str = Field(..., example="Enter Your Id")
    