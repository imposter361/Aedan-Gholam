import logging
import nextcord
from bot import client
from version import VERSION
from urlextract import URLExtract
from data import get_subscriptions


# on_message
@client.event
async def on_message(message):
    # gholam command added (auto reply)
    lower_message = str(message.content).lower()
    if ("gholam") in lower_message:
        if message.author != client.user:
            await message.reply(f"Gholametam v{VERSION}")

    # add "steam://openurl/" at the beginning of steam links.
    if message.author == client.user:
        return

    user_message = str(message.content)
    steam_store = "https://store.steampowered.com"
    steam_community = "https://steamcommunity.com"

    extractor = URLExtract()
    message_urls = extractor.find_urls(f"{user_message}")

    all_start_with_steam = all(
        item.startswith("steam://openurl/") for item in message_urls
    )

    steam_links = []
    if all_start_with_steam:
        return
    else:
        for i in message_urls:
            if i.startswith(steam_store) or i.startswith(steam_community):
                steam_links.append(f"steam://openurl/{i}\n")

    if steam_store in user_message or steam_community in user_message:
        try:
            # Check if the server has an active subscription or not
            subscriptions = get_subscriptions()
            if message.guild.id in subscriptions and subscriptions[message.guild.id]:
                URL = "".join(steam_links)
                embed = nextcord.Embed(description=URL)
                await message.reply(
                    f" Open directly in  <:steam_icon:1099351469674729553> ",
                    embed=embed,
                )

        except Exception as e:
            print(str(e) + "Exception happened in Steamlink edition")
            logging.error(str(e) + "Exception happened in Steamlink edition")
