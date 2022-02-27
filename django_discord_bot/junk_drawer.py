"""
A pile of useful stuff that doesn't have a better home.
"""
from __future__ import annotations

import asyncio
import functools
import traceback

from asgiref.server import StatelessServer


def exception_logger_async(func):
    @functools.wraps(func)
    async def _(*p, **kw):
        try:
            return await func(*p, **kw)
        except asyncio.CancelledError:
            raise
        except Exception:
            traceback.print_exc()
            raise
    return _


def exception_logger_sync(func):
    @functools.wraps(func)
    async def _(*p, **kw):
        try:
            return func(*p, **kw)
        except Exception:
            traceback.print_exc()
            raise
    return _


async def kill_task(task):
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception:
            traceback.print_exc()


class LifeSpanMixin:
    """
    Mixins for ASGI servers to act as a lifespan app.
    """
    async def start(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    def as_asgi(self):
        async def app(scope, receive, send):
            """
            Wraps the server as an ASGI lifespan app.
            """
            if scope['type'] == 'lifespan':
                while True:
                    message = await receive()
                    if message['type'] == 'lifespan.startup':
                        print(f"startup {self!r}")
                        await self.start()
                        await send({'type': 'lifespan.startup.complete'})
                    elif message['type'] == 'lifespan.shutdown':
                        print("shutdown {self!r}")
                        await self.close()
                        await send({'type': 'lifespan.shutdown.complete'})
                        return
        return app


class StatefulServer(LifeSpanMixin, StatelessServer):
    checker = None
    handler = None

    async def start(self):
        assert self.handler is self.checker is None
        self.checker = asyncio.create_task(self.application_checker())
        self.handler = asyncio.create_task(self.handle())

    async def close(self):
        await kill_task(self.handler)
        await kill_task(self.checker)
        self.checker = None
        self.handler = None
