"""
Low-level bits for talking to discord
"""
from __future__ import annotations

import asyncio
import dataclasses
import enum
import json
import random
import time

import aiohttp

from .junk_drawer import exception_logger_async, kill_task, StatefulServer


class Intent(enum.IntFlag):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    GUILD_SCHEDULED_EVENTS = 1 << 16

    # Combined Intents
    #: Everything except privledged
    BASIC = GUILDS | GUILD_BANS | GUILD_EMOJIS_AND_STICKERS | GUILD_INTEGRATIONS \
        | GUILD_WEBHOOKS | GUILD_INVITES | GUILD_MESSAGE_REACTIONS \
        | GUILD_MESSAGE_TYPING | DIRECT_MESSAGES | DIRECT_MESSAGE_REACTIONS \
        | DIRECT_MESSAGE_TYPING | GUILD_SCHEDULED_EVENTS
    #: Actually everything
    ALL = BASIC | GUILD_MEMBERS | GUILD_PRESENCES | GUILD_MESSAGES


class Op(enum.IntEnum):
    """
    Names for Discord Gateway Opcodes.

    These names are used for dynamic mappings to ASGI.
    """
    HEARTBEAT = 1  # C2S and S2C

    # Client to Server
    IDENTIFY = 2
    UPDATE_PRESENCE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    GUILD_REQUEST_MEMBERS = 8

    # Server to Client
    DISPATCH = 0
    HEARTBEAT_ACK = 11
    HELLO = 10
    RECONNECT = 7
    INVALID_SESSION = 9


#: Used by DiscordGateway internally
CONNECTED = object()


@dataclasses.dataclass
class DiscordMessage:
    op: Op
    t: str | None
    d: str | None
    s: int | None


asgi_type_to_op = {
    f"discord.{o.name.lower()}": o
    for o in Op
}


class DiscordGateway(StatefulServer):
    """
    ASGI server that connects to Discord's Gateway API and passes events to an
    ASGI application.
    """
    # TODO: Hooks for saving/loading session and seq (for seemless restarts)

    # Keeps a copy of the task responsible for heartbeating the connection.
    # Created by _ws_recv() and killed by handle()
    heartbeat_task = None

    # The sequence number of the last received message. Used in heartbeat and
    # resuming
    _last_seq = None

    # The monotonic time of the last time we saw a heartbeat ack.
    # According to the discord docs, this is how we should detect zombie
    # connections.
    _last_hb_ack = None

    # The session ID, used in resuming. Clear to disable resuming.
    session_id = None

    #: Indicates if the websocket is open and available
    ready: asyncio.Event

    def __init__(self, app, *, token, intents=Intent.BASIC):
        """
        app: ASGI app to handle more stuff
        """
        super().__init__(app)
        self.ready = asyncio.Event()

        # Configuration
        self.token = token
        self.intents = intents

    async def _connection_handler(self):
        """
        Does the low-level connecting and connection loops.

        Yields one of:
        * A websocket message (for CLOSE and CLOSED)
        * A dictionary of {op,ty,d,s} if we got data from Discord
        * CONNECTED, if we just reconnected
        """
        async with aiohttp.ClientSession() as self.session:
            while True:
                # TODO: Get gateway information from API
                # TODO: Take option for protocol version
                async with self.session.ws_connect('wss://gateway.discord.gg/?v=9&encoding=json') \
                           as self.sock:
                    while True:
                        msg = await self.sock.receive()
                        if msg.type == aiohttp.WSMsgType.CLOSE:
                            # We should handle this intelligently
                            # TODO: Read the code and log a more helpful message
                            print(f"{msg=}")
                            yield msg
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            yield msg
                            break
                        elif msg.type == aiohttp.WSMsgType.TEXT:
                            body = json.loads(msg.data)
                            op = Op(body['op'])
                            payload = body['d']
                            seq = body.get('s', None)
                            typ = body.get('t', None)
                            yield DiscordMessage(op=op, t=typ, d=payload, s=seq)
                        # TODO: Handle ETF
                        else:
                            print(f"{msg=}")

    @exception_logger_async
    async def handle(self):
        print("Starting WebSocket handler")
        app_queue = self.get_or_create_application_instance(None, {'type': 'discord'})
        self._last_seq = None
        try:
            async for msg in self._connection_handler():
                if msg is CONNECTED:
                    # We don't do anything on connecting
                    pass
                elif isinstance(msg, aiohttp.WSMessage):
                    if msg.type == aiohttp.WSMsgType.CLOSE:
                        # We should handle this intelligently
                        # TODO: Read the code and log a more helpful message
                        print(f"{msg=}")
                        self.ready.clear()
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        print(f"{msg=}")
                        self.ready.clear()
                        await kill_task(self.heartbeat_task)
                        await app_queue.put({'type': 'discord.disconnect'})
                elif isinstance(msg, DiscordMessage):
                    if msg.s is not None:
                        self._last_seq = msg.s
                    await self._ws_recv(app_queue, msg.op, msg.t, msg.d)
                else:
                    print(f"{msg=}")

        finally:
            await kill_task(self.heartbeat_task)
            await app_queue.put({'type': 'discord.disconnect'})
        print("Exiting WebSocket handler")

    async def _ws_recv(self, app_queue, op, typ, d):
        """
        Actually handle the parsed message
        """
        if op == Op.DISPATCH:
            if typ == 'READY':
                self.ready.set()
                # Save this for resuming
                self.session_id = d['session_id']
            elif typ == 'RESUMED':
                self.ready.set()
            await app_queue.put({'type': f'discord.{typ.lower()}', 'data': d})
        elif op == Op.HELLO:
            self.heartbeat_task = asyncio.ensure_future(
                self._beater(d['heartbeat_interval'] / 1000)
            )

            if self.session_id:
                # Attempting to resume
                print("Resuming")
                await self._ws_send(Op.RESUME, {
                    "token": self.token,
                    "session_id": self.session_id,
                    "seq": self._last_seq,
                })
            else:
                print("Fresh connection")
                await self._ws_send(Op.IDENTIFY, self._build_identify())
        elif op == Op.INVALID_SESSION:
            print("Bad session, re-identifying")
            # Per gateway docs, wait a random 1 to 5 seconds before re-auth
            await asyncio.sleep(random.uniform(1, 5))
            await self._ws_send(Op.IDENTIFY, self._build_identify())
        elif op == Op.RECONNECT:
            print("Reconnecting")
            await self.sock.close()
        elif op == Op.HEARTBEAT:
            # The server asked for an immediate heartbeat.
            # I'm not sure if we're supposed to delay the scheduled beat;
            # We'll just ignore that for now
            await self._ws_send(Op.HEARTBEAT, self._last_seq)
        elif op == Op.HEARTBEAT_ACK:
            self._last_hb_ack = time.monotonic()
        else:
            print(f"Unhandled message {op=} {typ=} {d=}")

    async def _shoot_zombie(self):
        await self.sock.close(4242)  # idk, no obvious close code for "hello?"

    def _build_identify(self):
        """
        Builds the identify blob
        """
        return {
            "token": self.token,
            "intents": int(self.intents),
            "properties": {
                "$os": "linux",  # TODO: Actually get the platform
                # TODO: Give some indication as to the actual service
                "$browser": "django-discord-bot",
                "$device": "django-discord-bot",
            },
        }

    async def _ws_send(self, op, d):
        """
        Send a message to the websocket
        """
        await self.sock.send_json({
            'op': op,
            'd': d,
        })

    async def application_send(self, scope, message):
        if scope['type'] == 'discord':
            print(f"Send to discord {scope=} {message=}")
            await self.ready.wait()
            t = message.pop('type')
            await self._ws_send(asgi_type_to_op[t], message)
        else:
            print(f"Unknown {scope=}")

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
            # Zombie check
            if (time.monotonic() - self._last_hb_ack) > interval:
                print("Zombie!")
                await self._shoot_zombie()
                return
