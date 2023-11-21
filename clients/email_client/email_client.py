import smtplib

from deploy.base import email_config


class EmailClient:
    _domain = email_config.domain
    _smtp_host = email_config.smtp_host
    _smtp_port = email_config.smtp_port
    _is_dev = email_config.is_dev

    def __init__(
        self,
        login,
        password,
        domain=None,
        smtp_host=None,
        smtp_port=None,
    ):
        self.server_login = login
        self.password = password
        self.domain = domain or self._domain
        self.smtp_host = smtp_host or self._smtp_host
        self.smtp_port = smtp_port or self._smtp_port

        self.from_email = f'{self.server_login}@{self.domain}'
        self.server = self.set_server()

    def set_server(self):
        if self._is_dev:
            return smtplib.SMTP(self.smtp_host, self.smtp_port)

        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        server.login(self.server_login, self.password)
        return server

    def send(self, to_addrs, msg):
        try:
            self.server.sendmail(
                from_addr=self.from_email,
                to_addrs=to_addrs,
                msg=msg,
            )
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            print(f'Не удалось отправить письмо. {reason}')
        else:
            print('Письмо отправлено!')

    def close(self):
        self.server.close()


email_client = EmailClient(
    login=email_config.email_login,
    password=email_config.email_password,
)
