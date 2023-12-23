import pika, time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

for i in range(0, 100):
    channel.basic_publish(exchange='', routing_key='hello', body=str(i))
    print(f" [x] Sent '{i}'")
    time.sleep(1)

connection.close()