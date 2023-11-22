import datetime

from . import models, schemas


async def get_notification(notification_id: str):
    return await models.Notification.get_by_id(notification_id)


async def get_notifications(skip: int = 0, limit: int = 100):
    return list(await models.Notification.select().offset(skip).limit(limit))


async def create_notification(notification: schemas.NotificationCreate):
    db_notification = await models.Notification.create(
        title=notification.title,
        text=notification.text,
        delivery_type=notification.delivery_type,
        send_at=notification.send_at,
    )

    return db_notification


async def update_notification(
    notification_id: str, notification: schemas.NotificationCreate
):
    await models.Notification.update(**notification.model_dump()).where(
        models.Notification.id == notification_id
    )
    return await get_notification(notification_id)


async def delete_notification(notification_id: str):
    await models.Notification.delete().where(models.Notification.id == notification_id)


async def update_notification_send_at(notification_id: str, send_at: datetime):
    await models.Notification.update(send_at=send_at).where(
        models.Notification.id == notification_id
    )
    return await get_notification(notification_id)


async def add_user_notifications(notification_id: str, notification_users: list):
    notification_users_list = [
        models.UserNotification(
            notification=notification_id,
            user=user,
        )
        for user in notification_users
    ]
    await models.UserNotification.bulk_create(notification_users_list)
    return True
