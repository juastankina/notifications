from enum import Enum

from pydantic_settings import BaseSettings


class DeliveryTypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'
    websocket = 'websocket'


class Settings(BaseSettings):
    project_name: str = 'notifications_admin'
    project_host: str = '127.0.0.1'
    project_port: int = 8000

    postgres_db: str = 'notifications'
    postgres_user: str = 'app'
    postgres_password: str = '12345'
    db_host: str = 'localhost'
    db_port: int = 5433
    db_url: str = f'asyncpg://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'

    log_level: str = 'debug'
    loggers_logging_level: str = 'info'

    page_size: int = 100

    NOTIFICATIONS_API_URL: str = 'http://notification_api:8000'
    NOTIFY_USERS_API_ENDPOINT: str = '/api/v1/notify_users'

    class Config:
        env_file = '.env'


settings = Settings()
