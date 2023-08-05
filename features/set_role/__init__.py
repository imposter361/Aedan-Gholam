import data
import logging
import nextcord
from bot import client


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True


# Add or remove user roles based on reactions
# Add role
async def set_role_based_on_reaction(added_reaction):
    if not _active:
        return False

    guild = nextcord.utils.find(
        lambda g: g.id == added_reaction.guild_id, client.guilds
    )
    reaction = added_reaction.emoji.name
    reactions = data.get_role_emoji(guild.id)
    set_role_message_id = data.get_role_message_id(guild.id)

    if (
        reaction in reactions.keys()
        and added_reaction.message_id == set_role_message_id
    ):
        role = nextcord.utils.get(guild.roles, name=reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(
                lambda m: m.id == added_reaction.user_id, guild.members
            )
            if member is not None:
                await member.add_roles(role)
                print(f"Role {role} added to {member}")
                logging.info(f"Role {role} added to {member}")


# Remove role
async def unset_role_based_on_reaction(removed_reaction):
    if not _active:
        return False

    guild = nextcord.utils.find(
        lambda g: g.id == removed_reaction.guild_id, client.guilds
    )
    reaction = removed_reaction.emoji.name
    reactions = data.get_role_emoji(guild.id)
    set_role_message_id = data.get_role_message_id(guild.id)
    if (
        reaction in reactions.keys()
        and removed_reaction.message_id == set_role_message_id
    ):
        role = nextcord.utils.get(guild.roles, name=reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(
                lambda m: m.id == removed_reaction.user_id, guild.members
            )
            if member is not None:
                await member.remove_roles(role)
                print(f"Role {role} removed from {member}")
                logging.info(f"Role {role} removed from {member}")
