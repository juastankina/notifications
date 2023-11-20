from enum import Enum

from pydantic_settings import BaseSettings


class DeliveryTypeEnum(str, Enum):
    email = 'email'
    sms = 'sms'
    websocket = 'websocket'


class Settings(BaseSettings):
    project_name: str = 'notifications'
    project_host: str = '127.0.0.1'
    project_port: int = 8000

    postgres_db: str = 'notifications'
    postgres_user: str = 'app'
    postgres_password: str = '12345'
    db_host: str = 'localhost'
    db_port: int = 5432

    rabbitmq_default_user: str = 'rmuser'
    rabbitmq_default_pass: str = 'rmpassword'
    rabbitmq_host: str = 'localhost'
    rabbitmq_port: int = 5672
    rabbitmq_url: str = f'amqp://{rabbitmq_default_user}:{rabbitmq_default_pass}@{rabbitmq_host}:{rabbitmq_port}/'

    log_level: str = 'debug'
    loggers_logging_level: str = 'info'

    page_size: int = 100

    USER_REGISTERED_EMAIL_QUEUE: str = 'email.user-registered'
    NOTIFICATION_EMAIL_QUEUE: str = 'email.notification'
    LIKES_EMAIL_QUEUE: str = 'email.new_likes'

    USER_NOTIFY_QUEUE: str = 'user_notify'

    QUEUES: list = [
        USER_REGISTERED_EMAIL_QUEUE,
        NOTIFICATION_EMAIL_QUEUE,
        LIKES_EMAIL_QUEUE,
        f'{DeliveryTypeEnum.email.value}.{USER_NOTIFY_QUEUE}',
        f'{DeliveryTypeEnum.sms.value}.{USER_NOTIFY_QUEUE}',
        f'{DeliveryTypeEnum.websocket.value}.{USER_NOTIFY_QUEUE}',
    ]

    AUTH_API_URL: str = 'http://auth-app:5000'
    AUTH_API_GET_USER_ENDPOINT: str = '/api/v1/auth/user'

    class Config:
        env_file = '.env'


settings = Settings()
