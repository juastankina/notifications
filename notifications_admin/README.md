# NOTIFICATIONS ADMIN API

---
Сервис для апи админки нотификаций
---
---
## Запуск
1. Запустить
```bash
docker-compose -f docker-compose.yml up  -d
```
Если надо поменять конфиг - создать в папке файл .env

Запустить c локально поднятой mongo_db
```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d
```
### Документация api

http://localhost/api/openapi

## Описание сервиса
В сервисе находится api для работы с нотификациями, отправка нотификации в RabbitMQ.

### Технологии
- python 3.11
- fast-api
- peewee-aio
- Docker
