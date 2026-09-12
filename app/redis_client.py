from typing import Optional

import redis.asyncio as aioredis

from app.config import settings


redis_client: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    """Инициализация клиента Redis. Вызывается на старте приложения."""
    global redis_client
    redis_client = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    # Проверяем подключение
    await redis_client.ping()


async def close_redis() -> None:
    """Закрытие клиента Redis. Вызывается на остановке приложения."""
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


def get_redis() -> aioredis.Redis:
    """FastAPI-зависимость: возвращает активный клиент Redis."""
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized")
    return redis_client
