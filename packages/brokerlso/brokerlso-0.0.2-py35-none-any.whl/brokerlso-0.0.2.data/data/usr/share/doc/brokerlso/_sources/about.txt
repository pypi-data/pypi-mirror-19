About
=====

*brokerlso* is a small library to create parts of Qpid Management Framework
(QMF) version 2 messages.

Legacy `qpid-python <https://pypi.python.org/pypi/qpid-python>`_
and associated packages provided the ability to manage an Apache Qpid broker.
The newer AMQP messaging toolkit,
`Qpid Proton <https://qpid.apache.org/proton/index.html>`_, does not provide
the same level of functionality.

*brokerlso* plugs in the gap by being focused solely on creating the parts
of an AMQP message that relate to QMF commands.

Look at tests and examples for more information on how to use *brokerlso*.

Name
----

Why *brokerlso*? It has two parts: *Broker* and *LSO*. *Broker* refers to the
Apache Qpid broker. *LSO* refers to
`Landing Signal Officer <https://en.wikipedia.org/wiki/Landing_Signal_Officer>`_.
*brokerlso* is meant to create QMFv2 messages to manage a Qpid broker.
