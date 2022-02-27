from __future__ import annotations

from asgiref.compatibility import guarantee_single_callable

from .plumbing import DiscordGateway, Intent
from . import local_config
from .junk_drawer import exception_logger_async
from .lifespan import multiplex_lifespan
from .schedule import ScheduleServer

discord_task = None


class ProtocolTypeRouter_WithLifespan:
    """
    Takes a mapping of protocol type names to other Application instances,
    and dispatches to the right one based on protocol name (or raises an error)

    Intelligently handles lifespan.
    """

    def __init__(self, application_mapping, extra_apps=()):
        """
        application_mapping: dict mapping scope types to applications
        extra_apps: List of apps that don't have protocols but should receive lifespan
        """
        self.application_mapping = application_mapping
        if 'lifespan' not in self.application_mapping:
            self.application_mapping['lifespan'] = multiplex_lifespan([
                *self.application_mapping.values(),
                *extra_apps
            ])

    async def __call__(self, scope, receive, send):
        if scope["type"] in self.application_mapping:
            application = guarantee_single_callable(
                self.application_mapping[scope["type"]]
            )
            return await application(scope, receive, send)
        else:
            raise ValueError(
                "No application configured for scope type %r" % scope["type"]
            )


class Bot_ProtocolTypeRouter(ProtocolTypeRouter_WithLifespan):
    """
    Wires up our opinions about what bots need.
    """
    def __init__(self, application_mapping, extra_apps=()):
        extra_apps = [*extra_apps, ScheduleServer().as_asgi()]
        if 'discord' in application_mapping:
            # FIXME: Config
            extra_apps += [DiscordGateway(
                application_mapping.pop('discord'),
                token=local_config.TOKEN, intents=Intent.ALL,
            ).as_asgi()]
        super().__init__(application_mapping, extra_apps)


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


app = Bot_ProtocolTypeRouter({
    'discord': discord_app
})
