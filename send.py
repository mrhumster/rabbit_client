#!/usr/bin/env python
import ssl
from ssl import SSLContext

import pika
from pika import PlainCredentials, SSLOptions

credentials = PlainCredentials(username='user', password='user')
context = ssl.create_default_context(cafile="testca/ca_certificate.pem")
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain("client/client_certificate.pem", "client/private_key.pem")
ssl_options = pika.SSLOptions(context, "omra-laptop")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='omra-laptop', port=5671, credentials=credentials, ssl_options=ssl_options))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()