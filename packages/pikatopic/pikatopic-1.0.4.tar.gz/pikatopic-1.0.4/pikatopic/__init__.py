#!/usr/bin/env python

import pika
import pika.credentials
import json
import os


# python2 and 3 string type check - from http://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility
try:
  basestring
except NameError:
  basestring = str

#
# These username/password/exchange settings work fine for a normal default RabbitMQ installation.
#
DEFAULT_USERNAME = os.environ.get('PIKATOPIC_USERNAME', 'guest')
DEFAULT_PASSWORD = os.environ.get('PIKATOPIC_PASSWORD', 'guest')
DEFAULT_EXCHANGE = os.environ.get('PIKATOPIC_EXCHANGE', 'amq.topic')

DEFAULT_HOST = os.environ.get('PIKATOPIC_HOST', 'localhost')


class PikaTopic(object):

    def __init__(self,
        host=None,
        username=None,
        password=None,
        exchange=None,
        no_rabbit_server=False,
        verbose=False):

        if not host:
            host = DEFAULT_HOST
        if not username:
            username = DEFAULT_USERNAME
        if not password:
            password = DEFAULT_PASSWORD
        if not exchange:
            exchange = DEFAULT_EXCHANGE

        self.host = host
        self.exchange = exchange
        self.username = username
        self.password = password

        self.verbose = verbose
        self.no_rabbit_server = no_rabbit_server

    def log(self, log_message):
        if self.verbose:
            print(log_message)

    def open(self):
        if self.no_rabbit_server:
            return self

        # print self.host, self.username, self.password

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            credentials=pika.credentials.PlainCredentials(
                username=self.username, 
                password=self.password,
                )
            ))

        if self.verbose:
            self.log("PikaTopic:open:connected to {0} as user {1}".format(self.host, self.username))

        self.channel = self.connection.channel()
        return self

    __enter__ = open    # support `with` construct

    def close(self, type=None, value=None, traceback=None):
        if self.no_rabbit_server:
            return

        self.connection.close()

    __exit__ = close    # support `with` construct



    def sendRaw(self, routing_key, message, content_type):
        self.log("PikaTopic:sendRaw:{0}:{1}:{2}".format(routing_key, content_type, message))
        if self.no_rabbit_server:
            return
        self.channel.basic_publish(exchange=self.exchange,
                      routing_key=routing_key,
                      body=message,
                      properties=pika.BasicProperties(content_type=content_type),
                      )

    def sendText(self, routing_key, message):
        if not isinstance(message, basestring):
            raise Exception('message must be a string, maybe use sendData() instead?')
        self.sendRaw(routing_key, message, 'text/plain')

    def sendData(self, routing_key, message):
        message = json.dumps(message)
        self.sendRaw(routing_key, message, 'application/json')


    def listen(self, handler, binding_keys):
        self.log("PikaTopic:listen")
        if self.no_rabbit_server:
            return

        # It's easy to accidentally give a string instead of a list
        # and since strings are iterable you get bad results. So,
        # we may as well be helpful here.
        if isinstance(binding_keys, basestring):
            binding_keys = [binding_keys]

        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        for binding_key in binding_keys:
            self.channel.queue_bind(exchange=self.exchange,
                               queue=queue_name,
                               routing_key=binding_key)

        def callback(ch, method, properties, body):

            body_data = None

            if properties.content_type == 'application/json':
                body_data = json.loads(body)

            if not handler(method.routing_key, body, body_data):
                # handler returned false, cancel the consumer
                self.channel.basic_cancel(self.consumer_tag)

        self.consumer_tag = self.channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        # loop - doesn't return unless the handler returns False
        self.channel.start_consuming()



def get_host_from_artella_config(file_name='/etc/artella/artella.conf'):
    host = None
    with open(file_name) as fp:
        c = json.load(fp)
        host = c.get('eventSystemRabbitHost')

    if not host:
        raise Exception("need Rabbit host name, try setting eventSystemRabbitHost in "+file_name)

    return host


if __name__ == "__main__":

    k = "testing.pylib.PikaTopic"

    #
    # no_rabbit_server -- means don't try to connect to a server, log calls to stdout
    #
    with PikaTopic(host='no_rabbit_server', verbose=True) as es:
        es.sendText(k, "not to a server")
        def h():
            pass
        es.listen(h, ['#']) # should return immediately


    with PikaTopic(host='172.17.0.2') as es:
        es.sendText(k, "high")
        es.sendData(k, {'cake':'is nice', 1000:True, 'a':[1,2,3]})
        es.sendText(k, "lo")

    es = PikaTopic(host='172.17.0.2')
    es.open()
    es.sendText(k, "other form")
    es.close()



