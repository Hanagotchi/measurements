import pika, time
from pika.exchange_type import ExchangeType

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fiufit-metrics-queue')

for i in range(0, 100):
    channel.basic_publish(exchange='fiutfit-metrics-exchange', routing_key='fiufit-metrics', body=str(i))
    print(f" [x] Sent '{i}'")
    time.sleep(1)

connection.close()