from __future__ import annotations

import datetime
from config import DeliveryTypeEnum

from typing import Any, Optional

import peewee
from pydantic import BaseModel, field_validator, UUID4
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class BaseDate(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class NotificationBase(BaseDate):
    title: str
    text: str
    delivery_type: DeliveryTypeEnum


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: UUID4
    send_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class NotificationUsers(BaseModel):
    notification_users: list[UUID4]


class NotificationSendAt(BaseDate):
    send_at: Optional[datetime] = None

    @field_validator('send_at')
    def validate_send_at(cls, send_at):
        if send_at:
            send_at = datetime.datetime.strptime(send_at, '%Y-%m-%d %H:%M:%S')
            if send_at < datetime.datetime.now():
                raise ValueError('date in the past')
        return send_at
