import logging
import random
import time
import uuid

import pika

from common.config import get_settings
from common.rabbit import build_parameters, publish_message, setup_topology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)

OPERATIONS = ["add", "subtract", "multiply", "divide"]


def main() -> None:
    cfg = get_settings()
    parameters = build_parameters(cfg)

    LOGGER.info("Producer connecting to RabbitMQ at %s:%s",
                cfg.rabbit_host, cfg.rabbit_port)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    setup_topology(channel, cfg)

    try:
        while True:
            payload = {
                "id": str(uuid.uuid4()),
                "operation": random.choice(OPERATIONS),
                "values": [round(random.uniform(1, 20), 2),
                           round(random.uniform(0, 10), 2)],
                "timestamp": time.time(),
            }
            publish_message(channel, cfg, payload)
            time.sleep(cfg.publish_interval)
    except KeyboardInterrupt:
        LOGGER.info("Producer stopped by user")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
