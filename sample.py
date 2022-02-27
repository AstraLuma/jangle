from django_discord_bot import Bot_ProtocolTypeRouter

import local_config

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
}, token=local_config.TOKEN)
