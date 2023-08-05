aiocall
=======

The missing call methods for python `asyncio <http://docs.python.org/3/library/asyncio>`_.

I found that python asyncio is lacking some basic methods to invoke calls:

.. code:: python

    call_soon_periodic(interval, callback, *args)
    call_later_periodic(delay, interval, callback, *args)

This module provides these methods.

Example:

.. code:: python

    import asyncio
    import aiocall

    def do_something(what):
        print('doing', what)

    timer = aiocall.call_later_periodic(0.5, 1.0, do_something, 'stuff')

    loop = asyncio.get_event_loop()
    loop.call_later(4.0, timer.cancel)
    loop.call_later(5.0, loop.stop)
    loop.run_forever()
    loop.close()

Output:

::

    doing stuff
    doing stuff
    doing stuff
    doing stuff
