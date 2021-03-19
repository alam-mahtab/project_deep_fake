import databases
import sqlalchemy
from functools import lru_cache
from api.user import config
#from api.user.models import metadata
from starlette.config import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import cloudinary

cloudinary.config(
    cloud_name = "alamcloud",
    api_key = "376629981897418",
    api_secret = "eSWZxKVVqisGZ_FIzCigU-JE_6I"
)

# Using Pydantic to load data
@lru_cache()
def setting():
    return config.setting()

def database_sqlite_url_config():
    #return str(setting().DB_URL)
    return str(setting().DB_STRINGPOST)

# # Using Stralette to load .env configuration
# def database_sqlite_url_config():
#     conf = Config(".env")
#     return str(conf("DB_URL"))

database = databases.Database(database_sqlite_url_config())
engine = sqlalchemy.create_engine(database_sqlite_url_config())
SessionLocal = sessionmaker(autoflush=False ,bind=engine, expire_on_commit=False)
#metadata.create_all(engine)
Base = declarative_base()