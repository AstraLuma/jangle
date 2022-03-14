from channels.consumer import AsyncConsumer


class Discord:
    """
    Friendly wrapper class used with signals and allows access for sending 
    gateway commands.
    """
    # Request guild members
    # Update presence
    # Update voice state
    # REST sessions (sync/async)


class DiscordConsumer(AsyncConsumer):
    async def discord_ready(self, event):
        print(event)

    async def discord_guild_create(self, event):
        print(event)

    async def discord_guild_member_chunk(self, event):
        print(event)

    async def discord_presence_update(self, event):
        print(event)

    async def discord_typing_start(self, event):
        print(event)

    async def discord_message_create(self, event):
        print(event)
