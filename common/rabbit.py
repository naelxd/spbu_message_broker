import json
import logging
from typing import Any

import pika

from common.config import Settings

LOGGER = logging.getLogger(__name__)


def build_parameters(cfg: Settings) -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(cfg.rabbit_user, cfg.rabbit_password)
    return pika.ConnectionParameters(
        host=cfg.rabbit_host,
        port=cfg.rabbit_port,
        credentials=credentials,
        heartbeat=30,
    )


def setup_topology(channel: pika.adapters.blocking_connection.BlockingChannel,
                   cfg: Settings) -> None:
    channel.exchange_declare(exchange=cfg.exchange,
                             exchange_type="direct", durable=True)
    channel.exchange_declare(exchange=cfg.dlx_exchange,
                             exchange_type="fanout", durable=True)

    args = {"x-dead-letter-exchange": cfg.dlx_exchange}
    channel.queue_declare(queue=cfg.queue, durable=True, arguments=args)
    channel.queue_bind(queue=cfg.queue, exchange=cfg.exchange,
                       routing_key=cfg.routing_key)

    channel.queue_declare(queue=cfg.dlq, durable=True)
    channel.queue_bind(queue=cfg.dlq, exchange=cfg.dlx_exchange)


def publish_message(channel: pika.adapters.blocking_connection.BlockingChannel,
                    cfg: Settings, payload: dict[str, Any]) -> None:
    body = json.dumps(payload)
    channel.basic_publish(
        exchange=cfg.exchange,
        routing_key=cfg.routing_key,
        body=body,
        properties=pika.BasicProperties(content_type="application/json",
                                        delivery_mode=2),
    )
    LOGGER.info("Published %s", body)
