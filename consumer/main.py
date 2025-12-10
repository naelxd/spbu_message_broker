import json
import logging

import pika

from common.config import get_settings
from common.operations import OperationError, apply_operation
from common.rabbit import build_parameters, setup_topology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)


def handle_message(channel: pika.adapters.blocking_connection.BlockingChannel,
                   method: pika.spec.Basic.Deliver,
                   properties: pika.BasicProperties, body: bytes, cfg) -> None:
    try:
        payload = json.loads(body.decode())
        result = apply_operation(payload["operation"], payload["values"])
        LOGGER.info("Processed task %s result=%s", payload.get("id"), result)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except (KeyError, json.JSONDecodeError,
            OperationError, ZeroDivisionError) as exc:
        LOGGER.error("Failed to process message: %s (%s)", body, exc)
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


def main() -> None:
    cfg = get_settings()
    parameters = build_parameters(cfg)

    LOGGER.info("Consumer connecting to RabbitMQ at %s:%s",
                cfg.rabbit_host, cfg.rabbit_port)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    setup_topology(channel, cfg)
    channel.basic_qos(prefetch_count=cfg.prefetch_count)

    def _callback(ch, method, properties, body):
        handle_message(ch, method, properties, body, cfg)

    channel.basic_consume(queue=cfg.queue, on_message_callback=_callback)
    LOGGER.info("Waiting for messages. Press Ctrl+C to exit.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        LOGGER.info("Consumer stopped by user")
    finally:
        if channel.is_open:
            channel.close()
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
