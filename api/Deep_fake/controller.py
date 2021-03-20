from fastapi import APIRouter, Depends, HTTPException, UploadFile , File
from . import crud, py_controller
from api.user.models import Users
import uuid, datetime
from sqlalchemy.orm import Session
from api.utils.db_utils import database
from api.utils import constant
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.user import models
from api.utils.db_utils import engine, SessionLocal
from starlette.staticfiles import StaticFiles
import cloudinary
import cloudinary.uploader

import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join
import shutil

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname ,'/static')

from pathlib import Path

current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static" 

# # @router.post("/deepfake/upload")
# # async def upload_photo_and_video(client_id:str,file_photo: UploadFile= File(...), file_video: UploadFile= File(...), db: Session = Depends(get_db)):
# #     result1 = cloudinary.uploader.upload(file_photo.file)
# #     url_photo = result1.get("url")
# #     result = cloudinary.uploader.upload(file_video.file, options = {})
# #     url_video = result.get("url")
# #     py_controller.generate_uploading_email([email])
# #     return crud.create_request_of_deepfake(db=db,client_id=client_id,url_photo=url_photo,url_video=url_video)

@router.post("/deepfake/upload")
async def upload_photo_and_video(email:str,file_photo: UploadFile= File(...), file_video: UploadFile= File(...), db: Session = Depends(get_db)):
    check = py_controller.check_user_exist(email,engine)
    if check:
        extension_pro = file_photo.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(file_photo.filename).suffix
        filename_pro = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
        with open("static/"+filename_pro, "wb") as image:
            shutil.copyfileobj(file_photo.file, image)
        print(dirname)
        print(images_path)
        url_photo = os.path.join(static_root_absolute, filename_pro)

        # extension_cover = file_cover.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        # if not extension_cover:
        #     return "Image must be jpg or png format!"
        suffix_cover =Path(file_video.filename).suffix
        filename_cover = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_cover )
        with open("static/"+filename_cover, "wb+") as video:
            shutil.copyfileobj(file_video.file, video)
        url_video = os.path.join(static_root_absolute, filename_cover)
        py_controller.generate_uploading_email([email])
        print("Success")
        return crud.create_request_of_deepfake(db=db,email=email,url_photo=url_photo,url_video=url_video)
    else:
        return  {"message":"Check your email-id"}