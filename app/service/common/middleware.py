import os
import time
import logging
import paho.mqtt.client as mqtt

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60
logger = logging.getLogger("rabbitmq_consumer")


class Middleware:
    def __init__(self):
        self._client = mqtt.Client()
        self._client.username_pw_set(os.environ.get("MQTT_USERNAME"),
                                     os.environ.get("MQTT_PASSWORD"))
        self._topic = None

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0 and self._client.is_connected():
            logger.info(f"Connected successfully with code {rc}: " +
                        f"{mqtt.connack_string(rc)}")
            if self._topic is not None:
                self._client.subscribe(self._topic)
                logger.info(f"Subscribed to '{self._topic}' topic")
        else:
            logger.info(f"Connect failed with code {rc}: " +
                        f"{mqtt.connack_string(rc)}")

    def _on_disconnect(self, client, userdata, rc):
        logger.info(f"Disconnected with result code {rc}: " +
                    f"{mqtt.error_string(rc)}")
        if rc == 0:
            logger.info(f"Disconnect successfully with code {rc}: " +
                        f"{mqtt.error_string(rc)}")
            return
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

    def _on_publish(self, client, userdata, mid):
        logger.info(f"Message publishd! Message id: {mid}")

    def listen_on(self, user_function, topic):
        self._topic = topic
        self._client.on_message = user_function

    def send_message(self, topic, msg, qos=2):
        result = self._client.publish(topic, msg, qos=qos)
        result.wait_for_publish()
        status = result[0]
        if status == 0:
            logger.info(f"Succesfully sent message '{msg}' to topic {topic} " +
                        f"with qos {qos} and message id {result[1]}. " +
                        "Result code: " +
                        f"{status}: {mqtt.error_string(status)}")
        else:
            logger.info(f"Failed to send message '{msg}' to topic {topic}. " +
                        f"with qos {qos} and message id {result[1]}. " +
                        "Result code: " +
                        f"{status}: {mqtt.error_string(status)}")

    def __del__(self):
        self.finish()

    def connect(self):
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish = self._on_publish
        self._client.connect(os.environ.get("MQTT_HOST"),
                             int(os.environ.get("MQTT_PORT")))
        logger.info("Connecting to " +
                    f"{os.environ.get('MQTT_HOST')}:" +
                    f"{os.environ.get('MQTT_PORT')}")

    def run(self):
        self._client.loop_start()
        while True:
            self._client.loop()
            if self._client.is_connected():
                logger.info("Connected to broker. Listening for messages or " +
                            "ready to send.")
                break

    def finish(self):
        self._client.loop_stop()
        self._client.disconnect()
