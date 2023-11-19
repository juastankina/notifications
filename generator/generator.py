import asyncio
import logging

from taskiq.api import run_scheduler_task
from taskiq_aio_pika import AioPikaBroker

from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler

from config.base import settings
from db.models import manager
from notifications_api import send_new_likes_notify
from db.db_service import get_likes_for_last_day

log = logging.getLogger(__name__)

broker = AioPikaBroker(settings.rabbitmq_url)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

cron_every_day = '0 12 * * *'


@broker.task(
    schedule=[{'cron': cron_every_day}], task_name='generate_likes_notifications'
)
async def generate_likes_notifications() -> None:
    log.info('Start generation new likes notifications')

    async with manager:
        async with manager.connection():
            async for like in get_likes_for_last_day():
                send_new_likes_notify(
                    user_id=like.user_id,
                    email=(await like.user).email,
                    likes_counter=like.counter,
                )

    log.info('Generation new likes notifications completed...')


async def main() -> None:
    await broker.startup()
    log.info('Broker started...')

    scheduler_task = asyncio.create_task(run_scheduler_task(scheduler))

    try:
        await scheduler_task
    except asyncio.CancelledError:
        log.info('Scheduler successfully exited.')

    await broker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
