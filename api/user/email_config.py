from pydantic import BaseSettings

class setting(BaseSettings):
    EMAIL_ID : str
    EMAIL_PWD: str

    class Config:
        env_file = "api/.env"
        env_file_encoding = "utf-8"