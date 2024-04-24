import os
import logging
from service.rabbitmq.consumer import Consumer
import firebase_admin
from firebase_admin import credentials

def main():
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)
    logger = logging.getLogger("rabbitmq_consumer")
    # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logging_level = os.environ.get("LOGGING_LEVEL")
    queue_name = os.environ.get("QUEUE_NAME")
    initialize_log(logging_level)
    consumer = Consumer(queue_name)
    logger.info("[RABBITMQ] Starting consumer...")
    consumer.run()


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
