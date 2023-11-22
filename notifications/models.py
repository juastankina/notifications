from pydantic import BaseModel

from config import DeliveryTypeEnum


class UserRegistered(BaseModel):
    user_id: str
    email: str
    tiny_url: str


class Notification(BaseModel):
    title: str
    text: str


class UserNotification(BaseModel):
    user_id: str
    title: str
    text: str
    delivery_type: DeliveryTypeEnum


class UsersNotification(BaseModel):
    users: list[str]
    title: str
    text: str
    delivery_type: DeliveryTypeEnum


class UserInfo(BaseModel):
    user_id: str
    email: str
    username: str


class SendUserNotification(UserInfo):
    title: str
    text: str


class Like(BaseModel):
    user_id: str
    email: str
    likes_counter: int
