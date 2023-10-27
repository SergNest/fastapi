from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    postgres_db: str = os.getenv('POSTGRES_DB', 'postgres')
    postgres_user: str = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'password')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', '5432'))

    sqlalchemy_database_url: str = f'postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:{postgres_port}/{postgres_db}'

    secret_key_jwt: str = os.getenv('SECRET_KEY_JWT', 'some_key')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')

    mail_username: str = os.getenv('MAIL_USERNAME', 'example@meta.ua')
    mail_password: str = os.getenv('MAIL_PASSWORD', 'password')
    mail_from: str = os.getenv('MAIL_FROM', 'example@meta.ua')
    mail_port: int = int(os.getenv('MAIL_PORT', '465'))
    mail_server: str = os.getenv('MAIL_SERVER', 'smtp.meta.ua')

    redis_host: str = os.getenv('REDIS_HOST', 'localhost')
    redis: int = int(os.getenv('REDIS', '6379'))

    cloudinary_name: str = os.getenv('CLOUDINARY_NAME', 'cloud_name')
    cloudinary_api_key: int = int(os.getenv('CLOUDINARY_API_KEY', '12345678'))
    cloudinary_api_secret: str = os.getenv('CLOUDINARY_API_SECRET', 'api_secret')

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf8'


settings = Settings()
