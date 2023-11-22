import requests

from config import DeliveryTypeEnum, settings


def notify_users(
    users: list,
    title: str,
    text: str,
    delivery_type: DeliveryTypeEnum,
) -> bool:
    request = requests.post(
        f'{settings.NOTIFICATIONS_API_URL}{settings.NOTIFY_USERS_API_ENDPOINT}',
        json={
            'users': users,
            'title': title,
            'text': text,
            'delivery_type': delivery_type,
        },
    )

    status_code = getattr(request, 'status_code')
    if status_code == 200:
        return True
    else:
        return False
