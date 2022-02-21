from __future__ import annotations

from .discord import DiscordGateway, Intent
from . import local_config
from .junk_drawer import exception_logger_async

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
async def app(scope, receive, send):
    global discord_task
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                print("startup")
                discord_task = DiscordGateway(
                    discord_app, token=local_config.TOKEN, intents=Intent.ALL,
                )
                await discord_task.start()
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                print("shutdown")
                await discord_task.close()
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:
        pass  # Handle other types
