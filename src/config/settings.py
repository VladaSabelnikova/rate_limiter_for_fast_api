"""Модуль содержит настройки для приложения."""

from pydantic import BaseSettings, BaseModel


class ConfigForModels(BaseSettings):  # TODO: Точно тут?

    """Класс с конфигом для всех моделей."""

    class Config:
        """
        Настройки pydantic.
        Подробнее см.
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


class RedisSettings(BaseModel):

    """Настройки RabbitMQ."""

    db_rate_limiter: int
    host: str
    port: int


class APISettings(BaseModel):

    """Настройки FastAPI."""

    host: str
    port: int


class Config(ConfigForModels):

    """Класс с конфигурацией проекта."""

    redis: RedisSettings
    api: APISettings


config = Config()
