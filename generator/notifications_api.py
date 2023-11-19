import requests

from config.base import settings


def send_new_likes_notify(
    email: str,
    user_id: str,
    likes_counter: int,
) -> bool:
    request = requests.post(
        f'{settings.NOTIFICATIONS_API_URL}{settings.NEW_LIKES_API_ENDPOINT}',
        json={
            'user_id': str(user_id),
            'email': email,
            'likes_counter': likes_counter,
        },
    )

    status_code = getattr(request, 'status_code')
    if status_code == 200:
        return True
    else:
        return False
