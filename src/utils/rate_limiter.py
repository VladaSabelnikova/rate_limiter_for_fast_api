"""Модуль содержит rate limiter."""
import datetime
from http import HTTPStatus as status
from typing import Callable

from aioredis import Redis
from fastapi import Depends, Header, HTTPException

from src.db.async_db_session.redis_client import rate_limiter_client
from src.utils.payload_parser import parse_payload_from_token


def requests_per_minute(limiter: int) -> Callable:

    """
    Функция-замыкание.

    Она пробрасывает ограничение кол-ва запросов в минуту (limitter) в область видимости асинхронной функции inner.
    В свою очередь inner выполняет rate limiter. Именно эту корутину будем использовать в Depends.

    Args:
        limiter: ограничение кол-ва запросов в минуту

    Returns:
        Вернёт корутину, которую будут использовать ручки API в Depends (для ограничения к ним запросов).
    """

    async def inner(
        redis_conn: Redis = Depends(rate_limiter_client.get_connect),
        authorization: str = Header(description='JWT token'),
        x_request_logger_name: str = Header(include_in_schema=False)
    ) -> None:
        """
        Функция для ограничения числа запросов в минуту.

        Args:
            redis_conn: соединение с Redis
            authorization: ключ в заголовке запроса (access токен пользователя)
            x_request_logger_name: имя логгера

        Raises:
            HTTPException:
                если кол-во запросов превысило лимит — гонит к чертям со словами извините, «Too Many Requests». :)
        """
        payload = await parse_payload_from_token(authorization)
        user_id = payload.user_id

        now = datetime.datetime.now()
        key = f'{x_request_logger_name}:{user_id}:{now.minute}'  # noqa: WPS237

        async with redis_conn.pipeline(transaction=True) as pipe:
            result_from_redis = await (
                pipe.incr(name=key, amount=1).expire(name=key, time=59).execute()  # type: ignore  # noqa: WPS432
            )

        request_number = result_from_redis[0]

        if request_number > limiter:
            raise HTTPException(status.TOO_MANY_REQUESTS.phrase, status.TOO_MANY_REQUESTS.value)

    return inner
