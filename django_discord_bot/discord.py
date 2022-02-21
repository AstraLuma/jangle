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
