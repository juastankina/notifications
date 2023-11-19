from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    postgres_db: str = 'notifications'
    postgres_user: str = 'app'
    postgres_password: str = '12345'
    db_host: str = 'postgres_notifications'
    db_port: int = 5432
    db_url: str = f'asyncpg://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'

    rabbitmq_default_user: str = 'rmuser'
    rabbitmq_default_pass: str = 'rmpassword'
    rabbitmq_host: str = 'rabbitmq_generator'
    rabbitmq_port: int = 5672
    rabbitmq_url: str = f'amqp://{rabbitmq_default_user}:{rabbitmq_default_pass}@{rabbitmq_host}:{rabbitmq_port}/'

    log_level: str = 'info'

    NOTIFICATIONS_API_URL: str = 'http://notification_api:8000'
    NEW_LIKES_API_ENDPOINT: str = '/api/v1/new_likes'

    class Config:
        env_file = '.env'


settings = Settings()
