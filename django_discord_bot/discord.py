"""
Low-level bits for talking to discord
"""

import enum


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
    # Ready
    # Resumed
    RECONNECT = 7
    INVALID_SESSION = 9
    # Guild Sync   
    # Channel Create
    # Channel Update
    # Channel Delete
    # Thread Create
    # Thread Update
    # Thread Delete
    # Thread List Sync
    # Thread Member Update
    # Thread Members Update
    # Channel Pins Update
    # Guild Create
    # Guild Update
    # Guild Delete
    # Guild Ban Add
    # Guild Ban Remove
    # Guild Emojis Update
    # Guild Stickers Update
    # Guild Integrations Update
    # Guild Member Add
    # Guild Member Remove
    # Guild Member Update
    # Guild Members Chunk
    # Guild Role Create
    # Guild Role Update
    # Guild Role Delete
    # Guild Scheduled Event Create
    # Guild Scheduled Event Update
    # Guild Scheduled Event Delete
    # Guild Scheduled Event User Add
    # Guild Scheduled Event User Remove
    # Integration Create
    # Integration Update
    # Integrationd Delete
    # Invite Create
    # Invite Delete
    # Message Create
    # Message Update
    # Message Delete
    # Message Delete Bulk
    # Message Reaction Add
    # Message Reaction Remove
    # Message Reaction Remove All
    # Message Reaction Remove Emoji
    # Presence Update
    # Typing Start
    # User Update
    # Voice State Update
    # Voice Server Update
    # Webhooks Update
    # Interaction Create
    # Stage Instance Create
    # Stage Instance Update
