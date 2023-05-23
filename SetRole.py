import logging
import nextcord
from bot import client
import data


# add or remove roles by reactions

# Add roles
@client.event
async def on_raw_reaction_add(role_set):
    guild = nextcord.utils.find(lambda g: g.id == role_set.guild_id, client.guilds)
    reaction = role_set.emoji.name
    reactions = data.get_role_emoji(guild.id)
    set_role_message_id = data.get_role_message_id(guild.id)

    if reaction in reactions.keys() and role_set.message_id == set_role_message_id:
        role = nextcord.utils.get(guild.roles, name=reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(
                lambda m: m.id == role_set.user_id, guild.members
            )
            if member is not None:
                await member.add_roles(role)
                print(f"Role {role} added to {member}")
                logging.info(f"Role {role} added to {member}")


# Remove roles
@client.event
async def on_raw_reaction_remove(role_unset):
    guild = nextcord.utils.find(lambda g: g.id == role_unset.guild_id, client.guilds)
    reaction = role_unset.emoji.name
    reactions = data.get_role_emoji(guild.id)
    set_role_message_id = data.get_role_message_id(guild.id)
    if reaction in reactions.keys() and role_unset.message_id == set_role_message_id:
        role = nextcord.utils.get(guild.roles, name=reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(
                lambda m: m.id == role_unset.user_id, guild.members
            )
            if member is not None:
                await member.remove_roles(role)
                print(f"Role {role} removed from {member}")
                logging.info(f"Role {role} removed from {member}")
