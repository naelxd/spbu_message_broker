import os
from dataclasses import dataclass


@dataclass
class Settings:
    rabbit_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbit_port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbit_user: str = os.getenv("RABBITMQ_USER", "guest")
    rabbit_password: str = os.getenv("RABBITMQ_PASSWORD", "guest")

    exchange: str = os.getenv("EXCHANGE_NAME", "tasks")
    dlx_exchange: str = os.getenv("DLX_EXCHANGE_NAME", "tasks.dlx")
    queue: str = os.getenv("QUEUE_NAME", "tasks.queue")
    dlq: str = os.getenv("DLQ_NAME", "tasks.dlq")
    routing_key: str = os.getenv("ROUTING_KEY", "math")

    publish_interval: float = float(os.getenv("PUBLISH_INTERVAL", "3"))
    prefetch_count: int = int(os.getenv("PREFETCH_COUNT", "10"))


def get_settings() -> Settings:
    return Settings()

