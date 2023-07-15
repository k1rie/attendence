from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    backend_url: str
    database_url: str
    smtp_user: str
    smtp_password: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_secret_key: str

    class Config:
        env_file = '.env'


settings = Settings()
