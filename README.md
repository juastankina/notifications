# notifications

Задания:
1) Реализуйте в своём сервисе модуль, отвечающий за генерацию и отправку персонализированных писем.
2) Реализуйте модуль для работы с Websocket.
3) Отдел маркетинга запускает новую рекламную кампанию. Нужно привлечь внимание пользователей к новым фичам 
онлайн-кинотеатра и увеличить конверсию в покупку новых фильмов. Для этого каждому пользователю необходимо 
отправить письмо с информацией и данными.
Технически требуется загрузить все письма в очередь на рассылку и полностью обработать её.
4) Реализуйте рассылку welcome-писем пользователям после регистрации в онлайн-кинотеатре. Welcome-письмо
обычно содержит приветственное сообщение и инструкции, как подтвердить email, указанный при регистрации.
5) Доработать CI

Запуск локального почтового сервера:
```bash
sudo python -m smtpd -n -c DebuggingServer localhost:25 
```

Запуск воркера-обработчика
```bash
python worker/reciever.py
```