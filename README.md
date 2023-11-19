# NOTIFICATIONS

### Локальный почтовый сервер
Запуск:
```bash
sudo python -m smtpd -n -c DebuggingServer localhost:25 
```
### Общие БД и RabbitMQ
Запуск:
```bash
docker-compose up --build -d
```


### 1. Генерация писем
Добавить `.env` в `/generator/config/` (пример: `/generator/config/.env.example`)

Запуск:
```bash
cd generator
docker-compose up --build -d
```

### 2. WebSocket
См. `/websocket_server/README.md`

### 3. API для отправки нотификаций в Воркер
См. `/notifications/README.md`

### 4. Воркер-обработчик
Получение событий из RabbitMQ и в дальнейшем отправка email.
Запуск:
```bash
python worker/receiver.py
```
