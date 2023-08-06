from asyncio.events import get_event_loop
from functools import wraps
import asyncio

from safepy.handle_bounded_methods import handle_bounded_methods


class TimeoutError(Exception):
    pass


def timeout(time):
    @handle_bounded_methods
    def decorator(function):

        @wraps(function)
        async def wrapper(*args, **kwargs):
            loop = kwargs.get('loop')
            if loop is None:
                loop = get_event_loop()

            await asyncio.wait_for(function(*args, **kwargs), time, loop=loop)

        return wrapper

    return decorator
