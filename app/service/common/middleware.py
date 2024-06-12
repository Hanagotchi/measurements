import os
import time
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger("rabbitmq_consumer")
logging.getLogger("pika").setLevel(logging.WARNING)

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


class Middleware:
    def __init__(self):
        self._client = mqtt.Client()
        self._client.username_pw_set(os.environ.get("MQTT_USERNAME"),
                                     os.environ.get("MQTT_PASSWORD"))
        self._topic = None

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected successfully")
            if self._topic is not None:
                self._client.subscribe(self._topic)
                logger.info(f"[x] Subscribed to {self._topic}")
        else:
            logger.info(f"Connect failed with code {rc}")

    def _on_disconnect(client, userdata, rc):
        logger.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logger.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logger.info("Reconnected successfully!")
                return
            except Exception as err:
                logger.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logger.info("Reconnect failed after %s attempts. Exiting...",
                    reconnect_count)

    def listen_on(self, user_function, topic):
        self._topic = topic
        self._client.on_connect = self._on_connect
        self._client.on_message = user_function
        self._client.on_disconnect = self._on_disconnect

    def send_message(self, topic, msg):
        result = self._client.publish(topic, msg)
        status = result[0]
        if status == 0:
            logger.info(f"Send `{msg}` to topic `{topic}`")
        else:
            logger.info(f"Failed to send message to topic {topic}")

    def __del__(self):
        self._client.disconnect()

    def connect(self):
        self._client.connect(os.environ.get("MQTT_HOST"),
                             int(os.environ.get("MQTT_PORT")))

    def run(self):
        self._client.loop_start()
        
    def finish(self):
        self._client.disconnect()
