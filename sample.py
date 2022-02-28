from jangle import Bot_ProtocolTypeRouter, schedule

import local_config


def check_in_sync():
    print("Checking in, synchronously!")


async def check_in_async():
    print("Checking in, asynchronously!")


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


schedule.every(1).minute.do(check_in_sync)
schedule.every(1).minute.do(check_in_async)

app = Bot_ProtocolTypeRouter({
    'discord': discord_app
}, token=local_config.TOKEN)
