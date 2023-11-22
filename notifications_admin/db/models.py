import datetime
import uuid

from peewee import CompositeKey
from peewee_aio import AIOModel, fields

from .db import db


@db.register
class UserEmails(AIOModel):
    user_id = fields.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    email = fields.CharField()
    name = fields.CharField(null=True)


@db.register
class Notification(AIOModel):
    id = fields.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    title = fields.CharField()
    text = fields.TextField()
    delivery_type = fields.CharField()
    created_at = fields.DateTimeField(default=datetime.datetime.now)
    send_at = fields.DateTimeField(null=True)


@db.register
class UserNotification(AIOModel):
    user = fields.ForeignKeyField(UserEmails, backref='user_notifications')
    notification = fields.ForeignKeyField(Notification, backref='notification_users')

    class Meta:
        primary_key = CompositeKey('user', 'notification')
