from pydantic_settings import BaseSettings


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

    QUEUES: list = [USER_REGISTERED_EMAIL_QUEUE, NOTIFICATION_EMAIL_QUEUE]

    class Config:
        env_file = '.env'


settings = Settings()
