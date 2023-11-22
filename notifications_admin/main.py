import logging

import uvicorn

from api.v1 import notification
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from config import settings
from db.db import db
from db.models import Notification, UserEmails, UserNotification

log = logging.getLogger(__name__)

tags_metadata = [
    {
        'name': settings.project_name,
        'description': 'Notifications API',
    },
]

app = FastAPI(
    title='Notifications',
    description='API для работы с нотификациями - отправка нотификаций',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
)


@app.exception_handler(ValueError)
async def validation_error_exception_handler(request: Request, exc: ValueError):
    return ORJSONResponse(
        status_code=404,
        content={'message': f'Oops! {exc.args} did something. There goes a rainbow...'},
    )


async def create_tables(db):
    log.info('Create tables ....')
    async with db:
        async with db.connection():
            tables = [
                UserEmails,
                Notification,
                UserNotification,
            ]
            for table in tables:
                await table.create_table()


@app.on_event('startup')
async def startup():
    log.info('Startup ....')
    await create_tables(db)
    log.info('App running ....')


@app.on_event('shutdown')
async def shutdown():
    log.info('Shutdown ....')


app.include_router(notification.router, prefix='/api/v1', tags=['admin/notifications'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.project_host,
        port=settings.project_port,
        log_level=settings.log_level,
        reload=True,
    )
