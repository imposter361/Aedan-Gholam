from bot import client
from features.set_role import set_role_based_on_reaction, unset_role_based_on_reaction


@client.event
async def on_raw_reaction_add(added_reaction):
    await set_role_based_on_reaction(added_reaction)


@client.event
async def on_raw_reaction_remove(removed_reaction):
    await unset_role_based_on_reaction(removed_reaction)
