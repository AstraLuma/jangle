from django.dispatch import Signal as _Signal

# Ready https://discord.com/developers/docs/topics/gateway#ready
#
# The ready event is dispatched when a client has completed the initial handshake with the gateway
# (for new sessions). The ready event can be the largest and most complex event the gateway will 
# send, as it contains all the state required for a client to begin interacting with the rest of
# the platform.
#
# guilds are the guilds of which your bot is a member. They start out as unavailable when you 
# connect to the gateway. As they become available, your bot will be notified via Guild Create
# events.
#
# v (int): gateway version
# user (user object): information about the user including email
#     https://discord.com/developers/docs/resources/user#user-object
# guilds (array of Unavailable Guild objects): the guilds the user is in
#     https://discord.com/developers/docs/resources/guild#unavailable-guild-object
# session_id (string): used for resuming connections
# shard? (array of two integers (shard_id, num_shards)): the shard information associated with this session, if sent when identifying
# application (partial application object):  contains id and flags
#    https://discord.com/developers/docs/resources/application#application-object

#: ready(sender: Discord, *, v, user, guilds, session_id, shard=None, application)
ready = _Signal()

# Resumed https://discord.com/developers/docs/topics/gateway#resumed
#: resumed(sender: Discord)
resumed = _Signal()

# CHANNEL_CREATE https://discord.com/developers/docs/topics/gateway#channel-create
#: channel_create(sender: Discord, *, channel)
channel_create = _Signal()

# CHANNEL_UPDATE https://discord.com/developers/docs/topics/gateway#channel-update
#: channel_update(sender: Discord, *, channel)
channel_update = _Signal()

# CHANNEL_DELETE https://discord.com/developers/docs/topics/gateway#channel-delete
#: channel_delete(sender: Discord, *, channel)
channel_delete = _Signal()

# THREAD_CREATE https://discord.com/developers/docs/topics/gateway#thread-create
#: thread_create(sender: Discord, *, channel)
thread_create = _Signal()

# THREAD_UPDATE https://discord.com/developers/docs/topics/gateway#thread-update
#: thread_update(sender: Discord, *, channel)
thread_update = _Signal()

# THREAD_DELETE https://discord.com/developers/docs/topics/gateway#thread-delete
#: thread_delete(sender: Discord, *, channel)
thread_delete = _Signal()

# THREAD_LIST_SYNC https://discord.com/developers/docs/topics/gateway#thread-list-sync
#: thread_list_sync(sender: Discord, *, guild_id, channel_ids=None, threads, memberships)
thread_list_sync = _Signal()

# THREAD_MEMBER_UPDATE https://discord.com/developers/docs/topics/gateway#thread-member-update
#: thread_member_update(sender: Discord, *, membership)
thread_member_update = _Signal()

# THREAD_MEMBERS_UPDATE https://discord.com/developers/docs/topics/gateway#thread-members-update
#: thread_members_update(sender: Discord, *, thread_id, guild_id, count, added_memberships, removed_membership_ids)
thread_members_update = _Signal()

# CHANNEL_PINS_UPDATE https://discord.com/developers/docs/topics/gateway#channel-pins-update
#: channel_pins_update(sender: Discord, *, guild_id, channel_id, timestamp)
channel_pins_update = _Signal()

# GUILD_CREATE https://discord.com/developers/docs/topics/gateway#guild-create
#: guild_create(sender: Discord, *, guild)
guild_create = _Signal()

# GUILD_UPDATE https://discord.com/developers/docs/topics/gateway#guild-update
#: guild_update(sender: Discord, *, guild)
guild_update = _Signal()

# GUILD_DELETE https://discord.com/developers/docs/topics/gateway#guild-delete
#: guild_delete(sender: Discord, *, guild)
guild_delete = _Signal()

# GUILD_BAN_ADD https://discord.com/developers/docs/topics/gateway#guild-ban-add
#: guild_ban_add(sender: Discord, *, guild_id, user)
guild_ban_add = _Signal()

# GUILD_BAN_REMOVE https://discord.com/developers/docs/topics/gateway#guild-ban-remove
#: guild_ban_remove(sender: Discord, *, guild_id, user)
guild_ban_remove = _Signal()

# GUILD_EMOJIS_UPDATE https://discord.com/developers/docs/topics/gateway#guild-emojis-update
#: guild_emojis_update(sender: Discord, *, guild_id, emojis)
guild_emojis_update = _Signal()

# GUILD_STICKERS_UPDATE https://discord.com/developers/docs/topics/gateway#guild-stickers-update
#: guild_stickers_update(sender: Discord, *, guild_id, stickers)
guild_stickers_update = _Signal()

# GUILD_INTEGRATIONS_UPDATE https://discord.com/developers/docs/topics/gateway#guild-integrations-update
#: guild_integrations_update(sender: Discord)
guild_integrations_update = _Signal()

# GUILD_MEMBER_ADD https://discord.com/developers/docs/topics/gateway#guild-member-add
#: guild_member_add(sender: Discord, *, membership)
guild_member_add = _Signal()

# GUILD_MEMBER_REMOVE https://discord.com/developers/docs/topics/gateway#guild-member-remove
#: guild_member_remove(sender: Discord, *, guild_id, user)
guild_member_remove = _Signal()

# GUILD_MEMBER_UPDATE https://discord.com/developers/docs/topics/gateway#guild-member-update
#: guild_member_update(sender: Discord, *, guild_id, user, roles, nick=None, avatar, joined_at, premium_since=None, deaf=None, mute=None, pending=None, communication_disabled_until=None)
guild_member_update = _Signal()

# GUILD_MEMBERS_CHUNK https://discord.com/developers/docs/topics/gateway#guild-members-chunk
#: guild_members_chunk(sender: Discord, *, guild_id, members, chunk_index, chunk_count, not_found=None, presences=None, nonce=None)
guild_members_chunk = _Signal()

# GUILD_ROLE_CREATE https://discord.com/developers/docs/topics/gateway#guild-role-create
#: guild_role_create(sender: Discord, *, guild_id, role)
guild_role_create = _Signal()

# GUILD_ROLE_UPDATE https://discord.com/developers/docs/topics/gateway#guild-role-update
#: guild_role_update(sender: Discord, *, guild_id, role)
guild_role_update = _Signal()

# GUILD_ROLE_DELETE https://discord.com/developers/docs/topics/gateway#guild-role-delete
#: guild_role_delete(sender: Discord, *, guild_id, role_id)
guild_role_delete = _Signal()

# GUILD_SCHEDULED_EVENT_CREATE https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-create
#: guild_scheduled_event_create(sender: Discord, *, event)
guild_scheduled_event_create = _Signal()

# GUILD_SCHEDULED_EVENT_UPDATE https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-update
#: guild_scheduled_event_update(sender: Discord, *, event)
guild_scheduled_event_update = _Signal()

# GUILD_SCHEDULED_EVENT_DELETE https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-delete
#: guild_scheduled_event_delete(sender: Discord, *, event)
guild_scheduled_event_delete = _Signal()

# GUILD_SCHEDULED_EVENT_USER_ADD https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-user-add
#: guild_scheduled_event_user_add(sender: Discord, *, event_id, user_id, guild_id)
guild_scheduled_event_user_add = _Signal()

# GUILD_SCHEDULED_EVENT_USER_REMOVE https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-user-remove
#: guild_scheduled_event_user_remove(sender: Discord, *, event_id, user_id, guild_id)
guild_scheduled_event_user_remove = _Signal()

# INTEGRATION_CREATE https://discord.com/developers/docs/topics/gateway#integration-create
#: integration_create(sender: Discord, *, integration)
integration_create = _Signal()

# INTEGRATION_UPDATE https://discord.com/developers/docs/topics/gateway#integration-update
#: integration_update(sender: Discord, *, integration)
integration_update = _Signal()

# INTEGRATION_DELETE https://discord.com/developers/docs/topics/gateway#integration-delete
#: integration_delete(sender: Discord, *, integration_id, guild_id, application_id=None)
integration_delete = _Signal()

# INVITE_CREATE https://discord.com/developers/docs/topics/gateway#invite-create
#: invite_create(sender: Discord, *, channel_id, code, created_at, guild_id=None, inviter=None, max_age, max_uses, target_type=None, target_user=None, target_application=None, temporary, uses)
invite_create = _Signal()

# INVITE_DELETE https://discord.com/developers/docs/topics/gateway#invite-delete
#: invite_delete(sender: Discord, *, channel_id, guild_id=None, code)
invite_delete = _Signal()

# MESSAGE_CREATE https://discord.com/developers/docs/topics/gateway#message-create
#: message_create(sender: Discord, *, message)
message_create = _Signal()

# MESSAGE_UPDATE https://discord.com/developers/docs/topics/gateway#message-update
#: message_update(sender: Discord, *, message)

# MESSAGE_DELETE https://discord.com/developers/docs/topics/gateway#message-delete
#: message_delete(sender: Discord, *, message_id, channel_id, guild_id=None)
message_delete = _Signal()

# MESSAGE_DELETE_BULK https://discord.com/developers/docs/topics/gateway#message-delete-bulk
#: message_delete_bulk(sender: Discord, *, message_ids, channel_id, guild_id=None)
message_delete_bulk = _Signal()

# MESSAGE_REACTION_ADD https://discord.com/developers/docs/topics/gateway#message-reaction-add
#: message_reaction_add(sender: Discord, *, used_id, channel_id, message_id, guild_id=None, member=None, emoji)
message_reaction_add = _Signal()

# MESSAGE_REACTION_REMOVE https://discord.com/developers/docs/topics/gateway#message-reaction-remove
#: message_reaction_remove(sender: Discord, *, user_id, channel_id, message_id, guild_id=None, emoji)
message_reaction_remove = _Signal()

# MESSAGE_REACTION_REMOVE_ALL https://discord.com/developers/docs/topics/gateway#message-reaction-remove-all
#: message_reaction_remove_all(sender: Discord, *, channel_id, message_id, guild_id=None)
message_reaction_remove_all = _Signal()

# MESSAGE_REACTION_REMOVE_EMOJI https://discord.com/developers/docs/topics/gateway#message-reaction-remove-emoji
#: message_reaction_remove_emoji(sender: Discord, *, channel_id, guild_id=None, message_id, emoji)
message_reaction_remove_emoji = _Signal()

# PRESENCE_UPDATE https://discord.com/developers/docs/topics/gateway#presence-update
#: presence_update(sender: Discord, *, user, guild_id, status, activities, client_status)
presence_update = _Signal()

# TYPING_START https://discord.com/developers/docs/topics/gateway#typing-start
#: typing_start(sender: Discord, *, channel_id, guild_id=None, user_id, timestamp, member=None)
typing_start = _Signal()

# USER_UPDATE https://discord.com/developers/docs/topics/gateway#user-update
#: user_update(sender: Discord, *, user)
user_update = _Signal()

# VOICE_STATE_UPDATE https://discord.com/developers/docs/topics/gateway#voice-state-update
#: voice_state_update(sender: Discord, *, voice_state)
voice_state_update = _Signal()

# VOICE_SERVER_UPDATE https://discord.com/developers/docs/topics/gateway#voice-server-update
#: voice_server_update(sender: Discord, *, token, guild_id, endpoint)
voice_server_update = _Signal()

# WEBHOOKS_UPDATE https://discord.com/developers/docs/topics/gateway#webhooks-update
#: webhooks_update(sender: Discord, *, guild_id, channel_id)
webhooks_update = _Signal()

# INTERACTION_CREATE https://discord.com/developers/docs/topics/gateway#interaction-create
#: interaction_create(sender: Discord, *, interaction)
interaction_create = _Signal()

# STAGE_INSTANCE_CREATE https://discord.com/developers/docs/topics/gateway#stage-instance-create
#: stage_instance_create(sender: Discord, *, stage)
stage_instance_create = _Signal()

# STAGE_INSTANCE_UPDATE https://discord.com/developers/docs/topics/gateway#stage-instance-delete
#: stage_instance_update(sender: Discord, *, stage)
stage_instance_update = _Signal()

# STAGE_INSTANCE_DELETE https://discord.com/developers/docs/topics/gateway#stage-instance-update
#: stage_instance_delete(sender: Discord, *, stage)
stage_instance_delete = _Signal()
