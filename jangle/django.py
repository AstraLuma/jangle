from channels.consumer import AsyncConsumer

from . import signals


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
        data = event['data']
        signals.ready.send_robust(
            Discord(),
            v=data['v'],
            user=data['user'],
            guilds=data['guilds'],
            session_id=data['session_id'],
            shard=data.get('shard', None),
            application=data['application'],
        )

    async def discord_resumed(self, event):
        print(event)
        signals.resumed.send_robust(Discord())

    async def discord_channel_create(self, event):
        print(event)
        data = event['data']
        signals.channel_create.send_robust(Discord(), channel=data)

    async def discord_channel_update(self, event):
        print(event)
        data = event['data']
        signals.channel_update.send_robust(Discord(), channel=data)

    async def discord_channel_delete(self, event):
        print(event)
        data = event['data']
        signals.channel_delete.send_robust(Discord(), channel=data)

    async def discord_thread_create(self, event):
        print(event)
        data = event['data']
        signals.thread_create.send_robust(Discord(), channel=data)

    async def discord_thread_delete(self, event):
        print(event)
        data = event['data']
        signals.thread_delete.send_robust(Discord(), channel=data)

    async def discord_thread_list_sync(self, event):
        print(event)
        data = event['data']
        signals.thread_list_sync.send_robust(
            Discord(), 
            guild_id=data['guild_id'],
            channel_ids=data.get('channel_ids', None),
            threads=data['threads'],
            members=data['members'],
        )

    async def discord_thread_member_update(self, event):
        print(event)
        data = event['data']
        signals.thread_member_update.send_robust(Discord(), membership=data)

    async def discord_thread_members_update(self, event):
        print(event)
        data = event['data']
        signals.thread_members_update.send_robust(
            Discord(),
            thread_id=data['id'],
            guild_id=data['guild_id'],
            count=data['member_count'],
            added_memberships=data.get('added_members', []),
            removed_membership_ids=data.get('removed_member_ids', []),
        )

    async def discord_channel_pins_update(self, event):
        print(event)
        data = event['data']
        signals.thread_member_update.send_robust(Discord(), membership=data)

    async def discord_guild_create(self, event):
        print(event)
        data = event['data']

    async def discord_guild_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_delete(self, event):
        print(event)
        data = event['data']

    async def discord_guild_ban_add(self, event):
        print(event)
        data = event['data']

    async def discord_guild_ban_remove(self, event):
        print(event)
        data = event['data']

    async def discord_guild_emojis_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_stickers_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_integrations_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_member_add(self, event):
        print(event)
        data = event['data']

    async def discord_guild_member_remove(self, event):
        print(event)
        data = event['data']

    async def discord_guild_member_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_members_chunk(self, event):
        print(event)
        data = event['data']

    async def discord_guild_role_create(self, event):
        print(event)
        data = event['data']

    async def discord_guild_role_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_role_delete(self, event):
        print(event)
        data = event['data']

    async def discord_guild_scheduled_event_create(self, event):
        print(event)
        data = event['data']

    async def discord_guild_scheduled_event_update(self, event):
        print(event)
        data = event['data']

    async def discord_guild_scheduled_event_delete(self, event):
        print(event)
        data = event['data']

    async def discord_guild_scheduled_event_user_add(self, event):
        print(event)
        data = event['data']

    async def discord_guild_scheduled_event_user_remove(self, event):
        print(event)
        data = event['data']

    async def discord_integration_create(self, event):
        print(event)
        data = event['data']

    async def discord_integration_update(self, event):
        print(event)
        data = event['data']

    async def discord_integration_delete(self, event):
        print(event)
        data = event['data']

    async def discord_invite_create(self, event):
        print(event)
        data = event['data']

    async def discord_invite_delete(self, event):
        print(event)
        data = event['data']

    async def discord_message_create(self, event):
        print(event)
        data = event['data']

    async def discord_message_delete(self, event):
        print(event)
        data = event['data']

    async def discord_message_delete_bulk(self, event):
        print(event)
        data = event['data']

    async def discord_message_reaction_add(self, event):
        print(event)
        data = event['data']

    async def discord_message_reaction_remove(self, event):
        print(event)
        data = event['data']

    async def discord_message_reaction_remove_all(self, event):
        print(event)
        data = event['data']

    async def discord_message_reaction_remove_emoji(self, event):
        print(event)
        data = event['data']

    async def discord_presence_update(self, event):
        print(event)
        data = event['data']
        signals.presence_update.send_robust(
            Discord(),
            user=data['user'],
            guild_id=data['guild_id'],
            status=data['status'],
            activities=data['activities'],
            client_status=data['client_status'],
        )

    async def discord_typing_start(self, event):
        print(event)
        data = event['data']

    async def discord_user_update(self, event):
        print(event)
        data = event['data']

    async def discord_voice_state_update(self, event):
        print(event)
        data = event['data']

    async def discord_voice_server_update(self, event):
        print(event)
        data = event['data']

    async def discord_webhooks_update(self, event):
        print(event)
        data = event['data']

    async def discord_interaction_create(self, event):
        print(event)
        data = event['data']

    async def discord_stage_instance_create(self, event):
        print(event)
        data = event['data']

    async def discord_stage_instance_delete(self, event):
        print(event)
        data = event['data']
