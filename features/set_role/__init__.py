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
        guild = client.get_guild(added_reaction.guild_id)
        member = added_reaction.member
        reaction_name = added_reaction.emoji.name

        reaction_role_dic = data.get_role_emoji(guild.id)
        set_role_message_id = data.get_role_message_id(guild.id)

        if (
            reaction_name not in reaction_role_dic.keys()
            or added_reaction.message_id != set_role_message_id
        ):
            return

        role = nextcord.utils.get(
            guild.roles, name=reaction_role_dic.get(reaction_name)
        )
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
        guild = client.get_guild(removed_reaction.guild_id)
        member = guild.get_member(removed_reaction.user_id)
        reaction_name = removed_reaction.emoji.name

        reaction_role_dic = data.get_role_emoji(guild.id)
        set_role_message_id = data.get_role_message_id(guild.id)

        if (
            reaction_name not in reaction_role_dic.keys()
            or removed_reaction.message_id != set_role_message_id
        ):
            return

        role = nextcord.utils.get(
            guild.roles, name=reaction_role_dic.get(reaction_name)
        )
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
