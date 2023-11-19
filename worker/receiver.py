import asyncio
import re

import orjson

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

from clients.email_client.email_messages import (
    NewLikesMessage,
    NewMessage,
    UserRegisteredMessage,
)
from deploy.base import settings

email_filter = re.compile(r'(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')


def check_email(email: str) -> bool:
    match = re.search(email_filter, email)
    if not match:
        return False
    return True


async def process_message(
    message: AbstractIncomingMessage,
) -> None:
    async with message.process():
        data = orjson.loads(message.body)
        NewMessage(to_email=['yu.astankina@yandex.ru']).send_message(data)
        print(data)
        await asyncio.sleep(1)


async def handle_register_user_message(
    message: AbstractIncomingMessage,
):
    async with message.process():
        data = orjson.loads(message.body)
        email = data.get('email')
        if not check_email(email):
            return
        # UserRegisteredMessage(to_email=[email]).send_message(link=data['tiny_url'])
        UserRegisteredMessage(to_email=['yu.astankina@yandex.ru']).send_message(
            link=data['tiny_url'],
        )
        await asyncio.sleep(1)


async def handle_new_like_message(
    message: AbstractIncomingMessage,
):
    async with message.process():
        data = orjson.loads(message.body)
        email = data.get('email')
        if not check_email(email):
            return
        # UserRegisteredMessage(to_email=[email]).send_message(link=data['tiny_url'])
        NewLikesMessage(to_email=['yu.astankina@yandex.ru']).send_message(
            counter=data['likes_counter'],
        )
        await asyncio.sleep(1)


async def register_queue(channel, queue_name: str):
    topic_user_registered_exchange = await channel.declare_exchange(
        queue_name,
        ExchangeType.TOPIC,
    )

    queue = await channel.declare_queue(
        queue_name,
        durable=True,
    )
    await queue.bind(
        topic_user_registered_exchange,
        routing_key=queue_name,
    )
    return queue


async def start():
    connection = await connect(settings.rabbitmq_url)

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    user_registered_queue = await register_queue(
        channel,
        settings.USER_REGISTERED_EMAIL_QUEUE,
    )
    notifications_queue = await register_queue(
        channel,
        settings.NOTIFICATION_EMAIL_QUEUE,
    )
    new_likes_queue = await register_queue(
        channel,
        settings.LIKES_EMAIL_QUEUE,
    )

    await user_registered_queue.consume(handle_register_user_message)
    await notifications_queue.consume(process_message)
    await new_likes_queue.consume(handle_new_like_message)

    return connection


async def main() -> None:
    connection = await start()
    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == '__main__':
    asyncio.run(main())
