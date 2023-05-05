import nextcord
from bot import *


#add or remove roles by reactions
#sample: 'emoji_name': 'role_name',
global reactions
reactions = {'csgo_icon':'CSGO',
            'minecraft_icon':'Minecraft',
            'valorant_icon':'Valorant',
            'r6_icon':'R6',
            'warzon_icon':'Warzone',
            'dst_icon':'Don\'t starve together' ,
            'dota2_icon':'Dota 2',
            'pubg_icon':'Pubg',
            'epic_icon':'Bounty Hunter',
            'amongus_icon':'Amongus',
            'fortnite_icon':'Fortnite',
            
            }

# Add roles
@client.event
async def on_raw_reaction_add(role_set):
    guild = nextcord.utils.find(lambda g: g.id == role_set.guild_id, client.guilds)
    reaction = role_set.emoji.name

    if reaction in reactions.keys() and role_set.message_id == int(SET_ROLE_MESSAGE_ID):
        role = nextcord.utils.get(guild.roles, name= reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(lambda m: m.id == role_set.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f"Role {role} added to {member}")
                logging.info(f"Role {role} added to {member}")
  
# Remove roles
@client.event
async def on_raw_reaction_remove(role_unset):
    guild = nextcord.utils.find(lambda g: g.id == role_unset.guild_id, client.guilds)
    reaction = role_unset.emoji.name
    if reaction in reactions.keys() and role_unset.message_id == int(SET_ROLE_MESSAGE_ID):
        role = nextcord.utils.get(guild.roles, name = reactions.get(reaction))
        if role is not None:
            member = nextcord.utils.find(lambda m: m.id == role_unset.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"Role {role} removed from {member}")
                logging.info(f"Role {role} removed from {member}")


def setup_set_role(bot):
    bot.event(on_raw_reaction_add)
    bot.event(on_raw_reaction_remove)