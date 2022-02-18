import asyncio
import contextlib
import functools
import json
import traceback

import aiohttp
from asgiref.server import StatelessServer


discord_task = None


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


class StatefulServer(StatelessServer):
    async def start(self):
        self.checker = asyncio.ensure_future(self.application_checker())
        self.handler = asyncio.ensure_future(self.handle())

    async def close(self):
        self.handler.cancel()
        self.checker.cancel()
        await asyncio.gather(self.handler, self.checker, return_exceptions=True)


class DiscordGateway(StatefulServer):
    def __init__(self, app):
        """
        app: ASGI app to handle more stuff
        """
        super().__init__(app)
        self.inner = contextlib.AsyncExitStack()

    @exception_logger_async
    async def handle(self):
        print("Starting WebSocket handler")
        app_queue = self.get_or_create_application_instance(None, {'type': 'discord'})
        async with aiohttp.ClientSession() as self.session, \
                   self.session.ws_connect('wss://gateway.discord.gg/?v=9&encoding=json') as self.sock:
            print(f"Have {self.sock=}")
            await app_queue.put({'type': 'discord.connect'})
            try:
                while True:
                    msg = await self.sock.receive()
                    print(f"{msg=}")
                    if msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.TEXT:
                        body = json.loads(msg.data)
                        print(f"{body=}")
            finally:
                await app_queue.put({'type': 'discord.disconnect'})
        print("Exiting WebSocket handler")

    async def application_send(self, scope, message):
        print(f"TODO: Send to discord {scope=} {message=}")


async def discord_app(scope, receive, send):
    if scope['type'] == 'discord':
        while True:
            message = await receive()
            print(f"Message from discord {message=}")


@exception_logger_async
async def app(scope, receive, send):
    global discord_task
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                print("startup")
                discord_task = DiscordGateway(discord_app)
                await discord_task.start()
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                print("shutdown")
                await discord_task.close()
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:
        pass  # Handle other types
