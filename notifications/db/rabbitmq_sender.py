import json
from functools import lru_cache

from aio_pika import DeliveryMode, ExchangeType, connect, Message

from config import settings
from models import Notification, UserRegistered


class SenderClient:
    TOPICS = {}

    def __init__(self, connect_settings):
        self.connection = None
        self.connect_settings = connect_settings

    async def get_connection(self):
        self.connection = await connect(self.connect_settings)
        return self.connection

    async def create_exchange(self, exchange_name):
        self.channel = await self.connection.channel()
        topic_exchange = await self.channel.declare_exchange(
            exchange_name,
            ExchangeType.TOPIC,
        )
        self.TOPICS[exchange_name] = topic_exchange

        return topic_exchange

    async def send(self, routing_key, message):
        connection = await self.get_connection()
        async with connection:
            self.topic = await self.create_exchange(routing_key)
            await self.topic.publish(message, routing_key=routing_key)


sender = SenderClient(settings.rabbitmq_url)


class BaseMessage:
    routing_key: str

    def __init__(
        self,
        message_body: dict,
        delivery_mode=None,
    ):
        if not delivery_mode:
            self.delivery_mode = DeliveryMode.PERSISTENT

        self.topic = None
        self.message_body = message_body
        self.sender: SenderClient = sender

    async def send(self):
        message = Message(
            json.dumps(self.message_body, indent=2).encode('utf-8'),
            # bytes(self.message_body, 'utf-8'),
            delivery_mode=self.delivery_mode,
        )
        await self.sender.send(self.routing_key, message)

        print(f' [x] Sent {message!r}')


class UserRegisteredMessage(BaseMessage):
    routing_key = settings.USER_REGISTERED_EMAIL_QUEUE

    def __init__(self, message_body: dict):
        super().__init__(message_body=message_body)


class NotificationMessage(BaseMessage):
    routing_key = settings.NOTIFICATION_EMAIL_QUEUE

    def __init__(self, message_body: dict):
        super().__init__(message_body=message_body)


class SendMessageService:
    @staticmethod
    async def send_user_registered_message(user: UserRegistered):
        user_registered = UserRegisteredMessage(user.model_dump())
        await user_registered.send()

    @staticmethod
    async def send_notification_message(notification: Notification):
        notification_message = NotificationMessage(notification.model_dump())
        await notification_message.send()


sender_service = SendMessageService()


@lru_cache()
def get_sender_service() -> SendMessageService:
    return sender_service
