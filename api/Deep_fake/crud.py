from sqlalchemy.orm import Session
from api.user import models
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import uuid
def create_request_of_deepfake(db: Session,client_id:str, url_photo:str, url_video:str):
    db_request = models.Fake(client_id=client_id,url_photo=url_photo,url_video=url_video)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request