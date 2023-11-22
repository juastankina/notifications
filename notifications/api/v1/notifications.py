import logging

from fastapi import APIRouter, Depends

from client.auth_api import get_user
from db.rabbitmq_sender import get_sender_service, SendMessageService
from models import (
    Like,
    Notification,
    SendUserNotification,
    UserNotification,
    UserRegistered,
    UsersNotification,
)

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


@router.post(
    '/notify_user',
    response_model=None,
    name='Отправить нотификацию клиенту с текстом в указанный в запросе канал',
)
async def notify_user(
    notification: UserNotification,
    sender: SendMessageService = Depends(get_sender_service),
):
    user_info = get_user(notification.user_id)
    await sender.send_notify_user_message(
        notification.delivery_type,
        SendUserNotification(**user_info.model_dump(), text=notification.text),
    )

    log.info(
        f'Notification request send {notification.title}, user={notification.user_id}'
    )


@router.post(
    '/notify_users',
    response_model=None,
    name='Отправить нотификацию списку клиентов с текстом в указанный в запросе канал',
)
async def notify_users(
    notifications: UsersNotification,
    sender: SendMessageService = Depends(get_sender_service),
):
    for user_id in notifications.users:
        user_info = get_user(user_id)
        await sender.send_notify_user_message(
            notifications.delivery_type,
            SendUserNotification(**user_info.model_dump(), text=notifications.text),
        )

    log.info(f'Notification request send {notifications.title}')
