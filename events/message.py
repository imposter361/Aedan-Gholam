from bot import client
from features import steam_link
from features.gholametam import gholametam
from nextcord import Message


# on_message
@client.event
async def on_message(message: Message):
    # "gholam" auto reply
    await gholametam(message)
    # generate steam:// link from https:// Steam links
    await steam_link.process(message)
