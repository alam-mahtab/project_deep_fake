from pydantic import BaseSettings

class setting(BaseSettings):
    #DB_URL:str
    DB_STRINGPOST : str

    class Config:
        env_file = "api/.env"
        env_file_encoding = "utf-8"

