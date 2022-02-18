import asyncio
import contextlib
import functools
import json
import random
import traceback

import aiohttp
from asgiref.server import StatelessServer

from .discord import Op, Intent
from . import local_config


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

    # Keeps a copy of the task responsible for heartbeating the connection.
    # Created by _ws_recv() and killed by handle()
    heartbeat_task = None

    # The sequence number of the last received message. Used in heartbeat and
    # resuming
    _last_seq = None

    def __init__(self, app):
        """
        app: ASGI app to handle more stuff
        """
        super().__init__(app)
        self.inner = contextlib.AsyncExitStack()

        # Configuration
        self.token = local_config.TOKEN
        self.intents = Intent.BASIC

    @exception_logger_async
    async def handle(self):
        print("Starting WebSocket handler")
        app_queue = self.get_or_create_application_instance(None, {'type': 'discord'})
        # TODO: Get gateway information from API
        # TODO: Handle resuming
        self._last_seq = None
        async with aiohttp.ClientSession() as self.session, \
                   self.session.ws_connect('wss://gateway.discord.gg/?v=9&encoding=json') as self.sock:
            print(f"Have {self.sock=}")
            try:
                while True:
                    msg = await self.sock.receive()
                    if msg.type == aiohttp.WSMsgType.CLOSE:
                        # We should handle this intelligently
                        print(f"{msg=}")
                    if msg.type == aiohttp.WSMsgType.CLOSED:
                        print(f"{msg=}")
                        break
                    elif msg.type == aiohttp.WSMsgType.TEXT:
                        body = json.loads(msg.data)
                        op = Op(body['op'])
                        payload = body['d']
                        if body.get('s', None) is not None:
                            self._last_seq = body['s']
                        typ = body.get('t', None)

                        await self._ws_recv(app_queue, op, typ, payload)
                    # TODO: Handle ETF
                    else:
                        print(f"{msg=}")

            finally:
                if self.heartbeat_task is not None:
                    self.heartbeat_task.cancel()
                    try:
                        await self.heartbeat_task
                    except asyncio.CancelledError:
                        pass
                    except Exception:
                        traceback.print_exc()

                await app_queue.put({'type': 'discord.disconnect'})
        print("Exiting WebSocket handler")

    async def _ws_recv(self, app_queue, op, typ, d):
        """
        Actually handle the parsed message
        """
        # TODO: Handle resuming
        # TODO: Handle heartbeating

        if op == Op.DISPATCH:
            await app_queue.put({'type': f'discord.{typ.lower()}', 'data': d})
        elif op == Op.HELLO:
            self.heartbeat_task = asyncio.ensure_future(self._beater(d['heartbeat_interval'] / 1000))
            await self._ws_send(Op.IDENTIFY, {
                "token": self.token,
                "intents": int(self.intents),
                "properties": {
                    "$os": "linux",  # FIXME
                    "$browser": "django-discord-bot",  # TODO: Give some indication as to the actual service
                    "$device": "django-discord-bot",
                },
            })
        elif op == Op.HEARTBEAT:
            # The server asked for an immediate heartbeat
            # I'm not sure if we're supposed to delay the scheduled beat
            # We'll just ignore that for now
            await self._ws_send(Op.HEARTBEAT, self._last_seq)
        else:
            print(f"Unhandled message {op=} {typ=} {d=}")

    async def _ws_send(self, op, d):
        """
        Send a message to the websocket
        """
        await self.sock.send_json({
            'op': op,
            'd': d,
        })

    async def application_send(self, scope, message):
        print(f"TODO: Send to discord {scope=} {message=}")

    async def _beater(self, interval):
        """
        Heartbeat task
        """
        # TODO: Handle heartbeat ack and zombie connections
        await asyncio.sleep(interval * random.random())
        print(f"Starting heartbeat every {interval} seconds")
        while True:
            await self._ws_send(Op.HEARTBEAT, self._last_seq)
            await asyncio.sleep(interval)


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
