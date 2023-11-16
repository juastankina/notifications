import logging

import uvicorn
from api.v1 import notifications
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import settings

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


@app.on_event('startup')
async def startup():
    log.info('Startup ....')
    log.info('App running ....')


@app.on_event('shutdown')
async def shutdown():
    log.info('Shutdown ....')


app.include_router(notifications.router, prefix='/api/v1', tags=['notifications'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.project_host,
        port=settings.project_port,
        log_level=settings.log_level,
        reload=True,
    )
