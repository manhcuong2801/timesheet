#!/usr/bin/env python
import pika
import time

authen = pika.credentials.PlainCredentials(username='guest', password='guest')

parameter = pika.ConnectionParameters(host='10.1.20.207', port=5672, credentials=authen, virtual_host='/')

connection = pika.BlockingConnection(parameters=parameter)

channel = connection.channel()

channel.exchange_declare(
    exchange='ose_dev_auth_exchange',
    exchange_type='fanout',
    durable=False
)
channel.queue_declare(queue='ose_dev_auth_rpc_queue', durable=False)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='ose_dev_auth_rpc_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
