PikaTopic - a convenience layer atop Pika for use with RabbitMQ topic exchanges
===============================================================================

Pika is a good general purpose library for interacting with a RabbitMQ
server. PikaTopic is a simpler, limited interface which can be used when
you just need to send or receive messages using a topic exchange.

Additionally, PikaTopic will handle json conversion when sending and
receiving data.

See https://github.com/AnimationMentor/pikatopic for more usage
examples.

Configuration
-------------

You will probably need to set the host name to connect to your RabbitMQ
server. The username, password and exchange are all set to defaults
which work for a generic server install.

Default values:

-  host is ``localhost`` OR the ``PIKATOPIC_HOST`` envariable if that is
   set
-  username is ``guest`` OR the ``PIKATOPIC_USERNAME`` envariable if
   that is set
-  password is ``guest`` OR the ``PIKATOPIC_PASSWORD`` envariable if
   that is set
-  exchange is ``amq.topic`` OR the ``PIKATOPIC_EXCHANGE`` envariable if
   that is set

These may be overridden by passing any of these arguments to the
``PikaTopic`` class initialiser or you can change them at the module
level by:

::

    import pikatopic

    pikatopic.DEFAULT_USERNAME = 'otheruser'
    pikatopic.DEFAULT_PASSWORD = 'secrt'
    pikatopic.DEFAULT_HOST = '172.17.0.2'
    pikatopic.DEFAULT_EXCHANGE = 'monster'

Pika Library
------------

Pikatopic depends on the pika libary.

-  http://pika.readthedocs.io/

Examples
--------

::

    from pikatopic import PikaTopic

    with PikaTopic(host='172.17.0.2') as pt:
        pt.sendData(
            "project.new",
            {
            'project_id':"12345-12345",
            'name':"The Amazing Adventures of Sausage Farts The Dog",
            'creator_id':"676867-45657",
            },
        )

::

    from pikatopic import PikaTopic

    def handler(routing_key, message, message_data):
        if message_data:
            print("%r data=%r" % (routing_key, message_data))
        else:
            print("%r text=%r" % (routing_key, message))
        return True


    with PikaTopic(host='172.17.0.2') as pt:
        pt.listen(handler, ['#'])

Reference
---------

This library provides a class, ``PikaTopic`` which can be used for
sending and receiving messages.

Unless using the ``with`` construct as in the examples above, you must
call ``open()`` and ``close()`` before and after the ``send...()`` and
``listen()`` functions.

Sending
~~~~~~~

::

    sendText(routing_key (string), message (string))

::

    sendData(routing_key (string), message (dict or list))

The ``sendData`` method converts the message to a json string and sets
the message content\_type property to application/json.

Receiving
~~~~~~~~~

::

    listen(handler (function), binding_keys (list of strings))

The ``listen`` method enters an event loop which normally does not
return.

It accepts a handler function which is called for each message received.

::

    handler(routing_key, message_text, message_data)

``message_text`` contains the raw text of the message. If the message is
json encoded then ``message_data`` contains the decoded dict otherwise
it is set to ``None``.

If the handler returns a false value, the ``listen()`` loop will return.

Serverless Testing
~~~~~~~~~~~~~~~~~~

Pass ``no_rabbit_server=True`` to the class initialiser to run without
connecting to a server.

This might be useful for testing or transition.

You may want to also set ``verbose=True``

Verbose
~~~~~~~

Pass ``verbose=True`` to the class initialiser to get messages sent to
stdout by the listen() and send...() functions.

Thanks, Artella!
================

This work was funded by Artella ( https://www.artella.com/ ).
