#! /usr/bin/env python3

import asyncio

def call_soon_periodic(interval, callback, *args, **kwargs):
    """Arrange for the `callback` to be called as soon as possible and
    periodically every `interval` seconds (either an int or float).

    `interval` is the delay between the end of one invocation of the callback
    and the start of the next invocation.

    An instance of `asyncio.Handle` is returned, which can be used to cancel
    the callback.

    The optional positional `args` will be passed to the callback when it is
    called. If you want the callback to be called with some named arguments,
    use a closure or `functools.partial()`.
    """
    async def coro():
        while True:
            callback(*args)
            await asyncio.sleep(interval)
    return asyncio.Task(coro(), **kwargs)

def call_later_periodic(delay, interval, callback, *args, **kwargs):
    """Arrange for the `callback` to be called after `delay` seconds
    periodically every `interval` seconds (both are either an int or float).

    `interval` is the delay between the end of one invocation of the callback
    and the start of the next invocation.

    An instance of `asyncio.Handle` is returned, which can be used to cancel
    the callback.

    The optional positional `args` will be passed to the callback when it is
    called. If you want the callback to be called with some named arguments,
    use a closure or `functools.partial()`.
    """
    async def coro():
        await asyncio.sleep(delay)
        while True:
            callback(*args)
            await asyncio.sleep(interval)
    return asyncio.Task(coro(), **kwargs)
