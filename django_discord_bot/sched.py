"""
AsyncIO/ASGI-based task scheduler. Exclusively in-process.

Mimics the api of https://schedule.readthedocs.io/en/stable/ but supports sync
and async and runs everything in the background.
"""
from __future__ import annotations

import asyncio

import schedule

from .junk_drawer import kill_task


Inf = float('inf')


class ScheduleServer:
    """
    ASGI "server" that runs schedules.
    """
    # Internally very similar to StatefulServer, but rips out most of it, since
    # we're not actually wrapping another app.
    handler = None

    async def handle(self):
        while True:
            schedule.run_pending()
            nextschedule = schedule.idle_seconds()
            await asyncio.sleep(nextschedule or 1)

    # Boilerplatey stuff
    async def start(self):
        assert self.handler is None
        self.handler = asyncio.create_task(self.handle())

    async def close(self):
        await kill_task(self.handler)
        self.handler = None

    async def __call__(self, scope, receive, send):
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
                    print(f"shutdown {self!r}")
                    await self.close()
                    await send({'type': 'lifespan.shutdown.complete'})
                    return
