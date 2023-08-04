import logging
import nextcord
from bot import client
from urlextract import URLExtract
from data.data import get_subscriptions


# on_message
def process(message):
    subscriptions = get_subscriptions()

    # Check if the server has an active subscription or not
    if message.guild.id not in subscriptions or not subscriptions[message.guild.id]:
        return None

    # add "steam://openurl/" at the beginning of steam links.
    if message.author == client.user:
        return None

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
        return None
    else:
        for i in message_urls:
            if i.startswith(steam_store) or i.startswith(steam_community):
                steam_links.append(f"steam://openurl/{i}\n")

    if steam_store in user_message or steam_community in user_message:
        try:
            URL = "".join(steam_links)
            embed = nextcord.Embed(description=URL)
            return {
                "response_text": "Open directly in  <:steam_icon:1099351469674729553>",
                "embed": embed,
            }

        except Exception as e:
            print(str(e) + "Exception happened in Steamlink edition")
            logging.error(str(e) + "Exception happened in Steamlink edition")

    return None
