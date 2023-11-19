from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
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

    log_level: str = 'info'
    loggers_logging_level: str = 'info'

    mongo_db_url: str = 'mongodb://mongodb:27017/'
    mongo_db_name: str = 'templates'

    USER_REGISTERED_EMAIL_QUEUE: str = 'email.user-registered'
    NOTIFICATION_EMAIL_QUEUE: str = 'email.notification'
    LIKES_EMAIL_QUEUE: str = 'email.new_likes'

    QUEUES: list = [
        USER_REGISTERED_EMAIL_QUEUE,
        NOTIFICATION_EMAIL_QUEUE,
        LIKES_EMAIL_QUEUE,
    ]

    class Config:
        env_file = '.env'


class EmailConfig(BaseSettings):
    email_login: str = 'yu.astankina'
    email_password: str

    domain: str = 'yandex.ru'
    smtp_host: str = 'smtp.yandex.ru'
    smtp_port: int = 465

    class Config:
        env_file = '.env'


settings = Settings()
email_config = EmailConfig()
