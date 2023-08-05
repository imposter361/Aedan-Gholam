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

    role = nextcord.utils.get(guild.roles, name=reaction_role_dic.get(reaction_name))
    if not role or not member:
        return

    await member.add_roles(role)
    print(f"Role {role} added to {member}")
    logging.info(f"Role {role} added to {member}")


# Remove role
async def unset_role_based_on_reaction(removed_reaction):
    if not _active:
        return False

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

    role = nextcord.utils.get(guild.roles, name=reaction_role_dic.get(reaction_name))
    if not role or not member:
        return

    await member.remove_roles(role)
    print(f"Role {role} removed from {member}")
    logging.info(f"Role {role} removed from {member}")