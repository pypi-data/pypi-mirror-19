PikaTopic - a convenience layer atop Pika for use with RabbitMQ topic exhanges
==============================================================================

Quickstart
----------

A RabbitMQ service ( https://www.rabbitmq.com/ ) must be running.

You also need the pika library.

::

    pip install pika

Run this, it will listen for new messages and not exit unless you kill
it.

::

    $ ./examples/recv.py

In another window, run this:

::

    $ ./examples/send.py

You should see output from ``recv.py``.

If your rabbit server is running on a different machine, you can set the
``PIKATOPIC_HOST`` environment variable. For example:

::

    $ PIKATOPIC_HOST=172.17.0.2 ./examples/recv.py

::

    $ PIKATOPIC_HOST=172.17.0.2 ./examples/send.py

Configuration
-------------

You will probably need to set the host name to connect to your RabbitMQ
server. The username, password and exchange are all set to defaults
which work for a generic server install.

Default values:

-  host is ``localhost`` OR the ``PIKATOPIC_HOST`` envariable if that is
   set
-  username is ``guest``
-  password is ``guest``
-  exchange is ``amq.topic``

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

::

    $ pip install pika

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
