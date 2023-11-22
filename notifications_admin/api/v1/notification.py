import datetime
import logging

from fastapi import APIRouter, Depends

from client.notifications_api import notify_users
from db import crud, db, schemas

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/notification',
    response_model=schemas.Notification,
    name='Создать рассылку',
    dependencies=[Depends(db.get_db)],
)
async def create_notification(
    notification: schemas.NotificationCreate,
):
    db_notification = await crud.create_notification(notification=notification)
    return db_notification


@router.get(
    '/notification/<notification_id>',
    response_model=schemas.Notification,
    name='Получить рассылку',
)
async def get_notification(notification_id: str):
    return await crud.get_notification(notification_id)


@router.get(
    '/notification/',
    response_model=list[schemas.Notification],
    name='Получить все рассылки',
)
async def get_notifications(skip: int = 0, limit: int = 100):
    return await crud.get_notifications(skip, limit)


@router.put(
    '/notification/<notification_id>',
    response_model=schemas.Notification,
    name='Отредактировать рассылку',
)
async def update_notification(
    notification_id: str,
    notification: schemas.NotificationCreate,
):
    return await crud.update_notification(notification_id, notification)


@router.delete(
    '/notification/<notification_id>',
    response_model=None,
    name='Удалить рассылку',
)
async def delete_notification(
    notification_id: str,
):
    await crud.delete_notification(notification_id)
    return 'ok'


@router.post(
    '/<notification_id>/add_users',
    response_model=str,
    name='Добавить пользователей в рассылку',
    dependencies=[Depends(db.get_db)],
)
async def add_notification_users(
    notification_id: str,
    users: schemas.NotificationUsers,
):
    await crud.add_user_notifications(
        notification_id=notification_id, notification_users=users.notification_users
    )
    return 'ok'


@router.post(
    '/<notification_id>/send',
    response_model=schemas.Notification,
    name='Отправить рассылку',
    dependencies=[Depends(db.get_db)],
)
async def send_notification(
    notification_id: str,
    send_at: schemas.NotificationSendAt,
):
    notification = await get_notification(notification_id=notification_id)

    users = [user.id async for user in notification.notification_users]
    if not users:
        raise ValueError('add users at first')

    if not send_at.send_at:
        # Если поле не передано, значит отправляем сейчас
        if notification.send_at:
            # Если уже было отправлено - ValidationError
            raise ValueError('notification already sent')

        notify_users(
            users=users,
            title=notification.title,
            text=notification.text,
            delivery_type=notification.delivery_type,
        )
        return await crud.update_notification_send_at(
            notification_id=notification_id, send_at=datetime.datetime.now()
        )

    else:
        return await crud.update_notification_send_at(
            notification_id=notification_id, send_at=send_at.send_at
        )
