import asyncio
import os
import logging
import json
from service.rabbitmq.consumer import Consumer
from firebase_admin import credentials, initialize_app


def main():
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
    cred = credentials.Certificate(json.loads(firebase_credentials))
    initialize_app(cred)

    logger = logging.getLogger("rabbitmq_consumer")
    logging_level = os.environ.get("LOGGING_LEVEL", "INFO")
    initialize_log(logging_level)

    loop = asyncio.get_event_loop()

    topic_name = os.environ.get("MQTT_TOPIC", "measurements")
    consumer = Consumer(topic_name)
    consumer.run()
    try:
        loop.run_forever()
    finally:
        loop.close()
    logger.info("[RABBITMQ] Starting consumer...")


def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
