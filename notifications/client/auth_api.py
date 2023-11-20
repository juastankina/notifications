import requests

from config import settings
from models import UserInfo


def get_user(
    user_id: str,
) -> UserInfo:
    request = requests.get(
        f'{settings.NOTIFICATIONS_API_URL}{settings.NOTIFICATIONS_API_ENDPOINT}/{user_id}',
    )
    status_code = getattr(request, 'status_code')
    if status_code == 200:
        return UserInfo(
            user_id=request.json().get('user_id'),
            email=request.json().get('email'),
            username=request.json().get('username'),
        )
