import data
import logging
import nextcord
from bot import client

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'set_role'")


# Add or remove user roles based on reactions
# Add role
async def set_role_based_on_reaction(added_reaction: nextcord.Reaction):
    if not _active:
        return False

    try:
        subscriptions = data.get_subscriptions()
        if not subscriptions.get(added_reaction.guild_id):
            return

        setrole_messages = data.setrole_messages_get(added_reaction.guild_id)
        if not setrole_messages:
            return

        target_message_key = f"{added_reaction.channel_id}/{added_reaction.message_id}"
        if not setrole_messages.get(target_message_key):
            return

        if added_reaction.user_id == client.user.id:  # Bot itself
            return

        guild = client.get_guild(added_reaction.guild_id)
        member = added_reaction.member
        emoji_key = added_reaction.emoji.name
        if added_reaction.emoji.id:
            emoji_key = str(added_reaction.emoji.id)

        emoji_role_dict = setrole_messages[target_message_key].get("emoji_role_dict")
        if not emoji_role_dict:
            return

        if not emoji_role_dict.get(emoji_key):
            return

        role = nextcord.utils.get(guild.roles, id=emoji_role_dict[emoji_key])
        if not role or not member:
            return

        await member.add_roles(role)
        _logger.debug(
            f"features/set_role: Role '{role}' was added to "
            + f"'{member.name}' ({member.id}) in '{guild.name}' ({guild.id})"
        )
    except:
        _logger.exception(
            f"features/set_role: Failed to set role for user ({added_reaction.user_id}) "
            + f"emoji: '{added_reaction.emoji.name}' in guild ({added_reaction.guild_id})"
        )


# Remove role
async def unset_role_based_on_reaction(removed_reaction: nextcord.Reaction):
    if not _active:
        return False

    try:
        subscriptions = data.get_subscriptions()
        if not subscriptions.get(removed_reaction.guild_id):
            return

        setrole_messages = data.setrole_messages_get(removed_reaction.guild_id)
        if not setrole_messages:
            return

        target_message_key = (
            f"{removed_reaction.channel_id}/{removed_reaction.message_id}"
        )
        if not setrole_messages.get(target_message_key):
            return

        if removed_reaction.user_id == client.user.id:  # Bot itself
            return

        guild = client.get_guild(removed_reaction.guild_id)
        member = guild.get_member(removed_reaction.user_id)
        emoji_key = removed_reaction.emoji.name
        if removed_reaction.emoji.id:
            emoji_key = str(removed_reaction.emoji.id)

        emoji_role_dict = setrole_messages[target_message_key].get("emoji_role_dict")
        if not emoji_role_dict:
            return

        if not emoji_role_dict.get(emoji_key):
            return

        role = nextcord.utils.get(guild.roles, id=emoji_role_dict[emoji_key])
        if not role or not member:
            return

        await member.remove_roles(role)
        _logger.debug(
            f"features/set_role: Role '{role}' was removed from "
            + f"'{member.name}' ({member.id}) in '{guild.name}' ({guild.id})"
        )
    except:
        _logger.exception(
            f"features/set_role: Failed to unset role for user ({removed_reaction.user_id}) "
            + f"emoji: '{removed_reaction.emoji.name}' in guild ({removed_reaction.guild_id})"
        )
