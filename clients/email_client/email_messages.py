from __future__ import annotations

import enum
import os
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from clients.email_client.email_client import email_client, EmailClient


class Templates(enum.Enum):
    NEW_LETTER = '/templates/mail.html'


class Message:
    def __init__(
        self,
        to_email: list[str],
        template: Templates,
        subject: str,
    ):
        self.to_email = to_email

        self.template = template
        self.subject = subject

        self.message = None

        self.server: EmailClient = email_client

    def send(self):
        self.server.send(
            to_addrs=self.to_email,
            msg=self.message.as_string(),
        )

    def generate(self, message_data: dict | None):
        message = EmailMessage()

        message['From'] = self.server.from_email
        message['To'] = ','.join(self.to_email)
        message['Subject'] = self.subject

        template = self.get_template()

        if message_data:
            output = template.render(**message_data)
        else:
            output = template.render()

        message.add_alternative(output, subtype='html')
        self.message = message
        return self.message

    def get_template(self):
        current_path = os.path.dirname(__file__)
        loader = FileSystemLoader(current_path)
        env = Environment(loader=loader)

        return env.get_template(self.template.value)

    def send_message(self, data):
        self.generate(data)
        self.send()


class NewMessage(Message):
    template = Templates.NEW_LETTER
    subject = 'Привет!'

    def __init__(self, to_email: list[str]):
        super().__init__(
            to_email=to_email, template=self.template, subject=self.subject
        )


def send_new_message(to_email):
    message = NewMessage(to_email=[to_email])
    data = {
        'title': 'Новое письмо!',
        'text': 'Произошло что-то интересное! :)',
        'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
    }
    message.send_message(data)


class NewFilmMessage(Message):
    template = Templates.NEW_LETTER
    subject = 'Вышел новый фильм'

    def __init__(self, to_email: list[str]):
        super().__init__(
            to_email=to_email, template=self.template, subject=self.subject
        )

    def send_message(self, film_name: str):
        data = {
            'title': f'Вышел новый фильм {film_name}',
            'text': 'Посмотри скорее! :)',
            'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
        }
        super().send_message(data)


class UserRegisteredMessage(Message):
    template = Templates.NEW_LETTER
    subject = 'Вы зарегистрировались'

    def __init__(self, to_email: list[str]):
        super().__init__(
            to_email=to_email, template=self.template, subject=self.subject
        )

    def send_message(self, link: str):
        data = {
            'title': 'Мы рады, что вы присоединились к нам!',
            'text': f'Для подтверждения электронной почты перейдите по ссылке {link}',
            'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
        }
        super().send_message(data)


class NewLikesMessage(Message):
    template = Templates.NEW_LETTER
    subject = 'У вас новые лайки'

    def __init__(self, to_email: list[str]):
        super().__init__(
            to_email=to_email, template=self.template, subject=self.subject
        )

    def send_message(self, counter: str):
        data = {
            'title': 'У вас появились новые лайки',
            'text': f'У вас {counter} новых лайков',
            'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
        }
        super().send_message(data)
