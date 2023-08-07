import logging
import nextcord
from bot import client
from urlextract import URLExtract
from data import get_subscriptions

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("Feature has been activated: 'steam_link'")


# on_message
async def process(message: nextcord.Message):
    if not _active:
        return False

    try:
        subscriptions = get_subscriptions()
        # Check if the server has an active subscription or not
        if message.guild.id not in subscriptions or not subscriptions[message.guild.id]:
            return False

        # add "steam://openurl/" at the beginning of steam links.
        if message.author == client.user:
            return False

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
            return False
        else:
            for i in message_urls:
                if i.startswith(steam_store) or i.startswith(steam_community):
                    steam_links.append(f"steam://openurl/{i}\n")

        if steam_store in user_message or steam_community in user_message:
            URL = "".join(steam_links)
            embed = nextcord.Embed(description=URL)
            await message.reply(
                "Open directly in  <:steam_icon:1099351469674729553>", embed=embed
            )
            return True

    except:
        _logger.exception()

    return False
