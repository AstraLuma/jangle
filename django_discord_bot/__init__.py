from __future__ import annotations

from .discord import DiscordGateway, Intent
from . import local_config
from .junk_drawer import exception_logger_async
from .lifespan import multiplex_lifespan
from .sched import ScheduleServer

discord_task = None


async def discord_app(scope, receive, send):
    if scope['type'] == 'discord':
        while True:
            message = await receive()
            print(f"Message from discord {message=}")
            if message['type'] == 'discord.ready':
                await send({
                    "type": "discord.guild_request_members",
                    "guild_id": 810010108347547708,
                    "query": "",
                    "limit": 0,
                })


@exception_logger_async
def app(scope, receive, send):
    global discord_task
    if scope['type'] == 'lifespan':
        return multiplex_lifespan([
            DiscordGateway(
                discord_app, token=local_config.TOKEN, intents=Intent.ALL,
            ),
            ScheduleServer(),
        ])(scope, receive, send)
    else:
        pass  # Handle other types
