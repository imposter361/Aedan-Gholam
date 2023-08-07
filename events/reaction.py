from bot import client
from features.set_role import set_role_based_on_reaction, unset_role_based_on_reaction
from nextcord import Reaction


@client.event
async def on_raw_reaction_add(added_reaction: Reaction):
    await set_role_based_on_reaction(added_reaction)


@client.event
async def on_raw_reaction_remove(removed_reaction: Reaction):
    await unset_role_based_on_reaction(removed_reaction)
