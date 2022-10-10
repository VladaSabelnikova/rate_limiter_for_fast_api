"""Модуль содержит функцию, для парсинга JWT токена."""
import base64

import orjson
from fastapi import Header

from src.models.tokens import AccessTokenData


async def parse_payload_from_token(
    authorization: str = Header(description='JWT token')
) -> AccessTokenData:
    """
    Функция распарсивает токен.

    Args:
        authorization: access токен

    Returns:
        Вернёт Pydantic модель с пользовательскими данными.
    """
    payload_str = base64.b64decode(authorization.split('.')[1]).decode()
    payload = orjson.loads(payload_str)
    return AccessTokenData(**payload['sub'])
