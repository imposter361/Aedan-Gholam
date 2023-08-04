from features import steam_link
from features.gholametam import gholametam
from bot import client


# on_message
@client.event
async def on_message(message):
    # gholam command added (auto reply)
    response = gholametam(message)
    if response:
        await message.reply(response)

    response = steam_link.process(message)
    if response:
        await message.reply(response["response_text"], embed=response["embed"])
