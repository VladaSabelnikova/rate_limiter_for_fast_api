## Rate limiter для использования в Depends FastAPI

Rate limiter ограничивает кол-во запросов для каждого пользователя в минуту.
Используется алгоритм Token bucket

### Принцип работы следующий:
1. Каждый пользователь может совершить не более N запросов в минуту к endpoint-у
2. Все N запросов могут быть обработаны одновременно, без задержки
3. Для каждого endpoint-а можно установить индивидуальный rate limit


### Инструкция по развёртыванию:
1. Клонировать проект
2. Установить зависимости `poetry install`
3. Запустить Redis `docker-compose up -d`
4. В папке src/use_case создать .env файл (образец в src/use_case/.env_example)
5. Стартовать FastAPI src/use_case/http_server.py

После этого можно запустить демонстрационный файл src/use_case/ddos_script.py
