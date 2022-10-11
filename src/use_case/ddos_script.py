"""Модуль содержит demo функцию для отправки запросов к API."""
from time import sleep

import httpx

from src.use_case.jwt_token import JWT_TOKEN


def main() -> None:

    """
    Функция отправляет запросы к API.

    Отправляем запросы с интервалом в 1.5 секунды и видим результат выполнения запроса.
    После превышения лимита запросов в минуту (rate_limit) API возвращает 429 Too Many Requests.
    После завершения текущей минуты можно вновь совершать запросы в пределах rate_limit.
    """

    url = 'http://localhost:8000/'
    headers = {'X-Request-Id': '12345', 'Authorization': JWT_TOKEN}

    for _ in range(50):  # Пробуем DDOS-ить API.
        response = httpx.get(url=url, headers=headers)
        print(response.status_code, response.text)
        sleep(1.5)


if __name__ == '__main__':
    main()
