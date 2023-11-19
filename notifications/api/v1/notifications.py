import logging

from fastapi import APIRouter, Depends

from db.rabbitmq_sender import get_sender_service, SendMessageService
from models import Like, Notification, UserRegistered

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/user_registered',
    response_model=None,
    name='Отправить нотификацию по регистрации нового пользователя',
)
async def user_registered(
    user: UserRegistered,
    sender: SendMessageService = Depends(get_sender_service),
):
    await sender.send_user_registered_message(user)

    log.info(f'Notification request send for user {user.user_id}')


@router.post(
    '/notify',
    response_model=None,
    name='Отправить нотификацию с текстом и заголовком',
)
async def notify(
    notification: Notification,
    sender: SendMessageService = Depends(get_sender_service),
):
    await sender.send_notification_message(notification)

    log.info(f'Notification request send {notification.title}')


@router.post(
    '/new_likes',
    response_model=None,
    name='Отправить нотификацию о последних лайках',
)
async def likes_notify(
    like: Like,
    sender: SendMessageService = Depends(get_sender_service),
):
    await sender.send_new_likes_message(like)

    log.info('New like notification request send')
