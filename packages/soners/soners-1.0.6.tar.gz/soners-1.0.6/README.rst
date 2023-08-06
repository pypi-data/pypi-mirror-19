======
soners
======

PySerial reader extension for Tornado

.. image:: https://badge.fury.io/py/soners.png
    :target: http://badge.fury.io/py/soners
.. image:: https://travis-ci.org/cpapazaf/soners.svg?branch=master
    :target: https://travis-ci.org/cpapazaf/soners

Usage
-----

Simple example::

    import tornado
    from soners.soners_server import SonersServer


    def temperature_handler(device, temperature):
        print(temperature)


    if __name__ == '__main__':
        my_sensor = SonersServer([('^T:(?P<temperature>.*)$', temperature_handler)])
        my_sensor.listen()
        tornado.ioloop.IOLoop.current().start()


Installation
------------

Or using last source::

    $ pip install git+git://github.com/cpapazaf/soners.git


Contribution
------------

Creating Issues
~~~~~~~~~~~~~~~

If you find a problem please create an 
issue in the `ticket-system`_
and describe what is going wrong or what you expect to happen.
If you have a full working example or a log file this is also helpful.
You should of course describe only a single issue in a single ticket and not 
mixing up several different things into a single issue.

Creating a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~

Before you create a pull request it is necessary to create an issue in
the `ticket-system`_ and describe what the problem is or what kind of 
feature you would like to add. Afterwards you can create an appropriate 
pull request.

It is required if you want to get a Pull request to be integrated into to squash your
commits into a single commit which references the issue in the commit message.

A pull request has to fulfill only a single ticket and should never create/add/fix
several issues in one, cause otherwise the history is hard to read and to understand 
and makes the maintenance of the issues and pull request hard.

License
-------

Distributed under the Apache License 2.0 license: http://opensource.org/licenses/Apache-2.0

.. _ticket-system: https://github.com/cpapazaf/soners/issues

