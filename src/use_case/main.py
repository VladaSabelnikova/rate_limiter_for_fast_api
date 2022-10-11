"""Модуль содержит demo FastAPI приложение."""
import uvicorn
from fastapi import FastAPI, Depends

from src.config.logging_settings import LOGGING
from src.config.settings import config
from src.use_case.startup_shutdown import startup, shutdown
from src.utils.rate_limiter import requests_per_minute

app = FastAPI(
    on_startup=[
        startup
    ],
    on_shutdown=[
        shutdown
    ],
)


@app.get('/', dependencies=[Depends(requests_per_minute(3))])
async def root() -> dict:
    """
    Demo endpoint, для демонстрации возможностей rate limiter-а.
    В данном случае пользователь не сможет обратиться к этому endpoint-у больше 3-х раз в минуту.

    Returns:
        Вернёт словарь, или исключение 429, если кол-во запросов превысило лимит.
    """
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.api.host,
        port=config.api.port,
        log_config=LOGGING,
    )
