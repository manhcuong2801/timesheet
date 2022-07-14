#!/usr/bin/env python
import pika
import sys

authen = pika.credentials.PlainCredentials(username='guest', password='guest')

parameter = pika.ConnectionParameters(host='10.1.20.207', port=5672, credentials=authen, virtual_host='/')

connection = pika.BlockingConnection(parameters=parameter)
channel = connection.channel()
channel.exchange_declare(
            exchange='ose_dev_auth_exchange',
            exchange_type='fanout',
            durable=True
        )

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.queue_declare(queue='ose_dev_auth_rpc_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    body=message,
    routing_key='',
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE, reply_to=callback_queue
    ))
print(" [x] Sent %r" % message)
connection.close()
