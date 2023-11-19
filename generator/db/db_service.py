import datetime
import logging

from db.models import Likes, UserEmails


today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)

# Создаем объект datetime для сегодня в 12:00
yesterday_at_noon = datetime.datetime.combine(yesterday, datetime.time(12, 0))
today_at_noon = datetime.datetime.combine(today, datetime.time(12, 0))

log = logging.getLogger(__name__)


def get_likes_for_last_day():
    return (
        Likes.select(Likes, UserEmails)
        .where(
            (Likes.updated_at > yesterday_at_noon) & (Likes.updated_at <= today_at_noon)
        )
        .join(UserEmails)
    )
