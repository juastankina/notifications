from pydantic import BaseModel


class UserRegistered(BaseModel):
    user_id: str
    email: str
    tiny_url: str


class Notification(BaseModel):
    title: str
    text: str


class Like(BaseModel):
    user_id: str
    email: str
    likes_counter: int
