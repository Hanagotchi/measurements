import pika
import os


class Middleware:

    def __init__(self):
        self._connection = (pika.BlockingConnection
                            (pika.ConnectionParameters(host=os.environ.get
                                                       ("RABBITMQ_HOST"))))
        self._channel = self._connection.channel()
        self._exit = False
        self._remake = False

    def create_queue(self, queue_name):
        self._channel.queue_declare(queue=queue_name)

    def _setup_message_consumption(self, queue_name, user_function):
        self._channel.basic_consume(queue=queue_name,
                                    on_message_callback=lambda channel,
                                    method, properties, body:
                                    (user_function(body),
                                     channel.basic_ack
                                     (delivery_tag=method.delivery_tag),
                                     self._verify_connection_end()))
        self._channel.start_consuming()

    def _verify_connection_end(self):
        if self._exit:
            self._channel.close()
            if self._remake:
                self._exit = False
                self._channel = self._connection.channel()

    def finish(self, open_new_channel=False):
        self._exit = True
        self._remake = open_new_channel

    # Work queue methods
    def listen_on(self, queue_name, user_function):
        self.create_queue(queue_name)
        self._channel.basic_qos(prefetch_count=30)
        self._setup_message_consumption(queue_name, user_function)

    def send_message(self, queue_name, message):
        self._channel.basic_publish(exchange='',
                                    routing_key=queue_name,
                                    body=message)

    def __del__(self):
        self._connection.close()
