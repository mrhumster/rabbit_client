#!/usr/bin/env python
import ssl

import pika, sys, os
from pika import PlainCredentials


def main():
    credentials = PlainCredentials(username='user', password='user')
    context = ssl.create_default_context(cafile="testca/ca_certificate.pem")
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain("client/client_certificate.pem", "client/private_key.pem")
    ssl_options = pika.SSLOptions(context, "omra-laptop")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='omra-laptop', credentials=credentials, ssl_options=ssl_options))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
