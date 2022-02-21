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


async def kill_task(task):
    if task is not None:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception:
            traceback.print_exc()


class StatefulServer(StatelessServer):
    async def start(self):
        self.checker = asyncio.ensure_future(self.application_checker())
        self.handler = asyncio.ensure_future(self.handle())

    async def close(self):
        self.handler.cancel()
        self.checker.cancel()
        await asyncio.gather(self.handler, self.checker, return_exceptions=True)
