import data
import logging
from bot import client
from bs4 import BeautifulSoup
from features._shared.helper import aiohttp_get

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'cs2_announcements'")
    from . import task


async def check_cs2_announcements_for_all_guilds():
    if not _active:
        return False

    last_announcement_date = None
    last_announcement_link = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.cs2_announcements_channel_id_get(guild_id)
        if not channel_id:
            continue

        if not last_announcement_date:
            (
                last_announcement_date,
                last_announcement_link,
            ) = await _get_last_cs2_announcement()
            if last_announcement_date == None:
                _logger.warning(
                    "features/cs2_announcements: No valid announcements link was found."
                )
                break

        await _send_cs2_announcement_for_guild(
            guild_id, channel_id, last_announcement_date, last_announcement_link
        )


async def check_cs2_announcements_for_guild(guild_id: int):
    if not _active:
        return

    subscriptions = data.get_subscriptions()
    if not subscriptions.get(guild_id):
        return

    channel_id = data.cs2_announcements_channel_id_get(guild_id)
    if not channel_id:
        return

    (
        last_announcement_date,
        last_announcement_link,
    ) = await _get_last_cs2_announcement()
    await _send_cs2_announcement_for_guild(
        guild_id, channel_id, last_announcement_date, last_announcement_link
    )


async def _get_last_cs2_announcement():
    _logger.debug("features/cs2_announcements: Getting last CS2 announcement...")

    last_announcement_date = None
    last_announcement_link = None
    url = "https://steamcommunity.com/games/CSGO/announcements/"

    try:
        response = await aiohttp_get(url)
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response, "html.parser")
        for element in soup.find_all("a"):
            if "Release Notes for" in element.string:
                print(element)
    


    except:
        _logger.exception("features/cs2_announcements: Could not get CS2 announcements links.")

    return last_announcement_date, last_announcement_link


async def _send_cs2_announcement_for_guild(guild_id, channel_id, klei_points):
    try:
        channel = client.get_channel(channel_id)
        if not channel:
            _logger.debug(
                "features/klei_points: Failed to get channel with id of: "
                + f"{channel_id} in guild: {guild_id}"
            )
            return

        sent_links = data.klei_links_get(guild_id)
        valid_sent_links = []

        for klei_point in klei_points:
            if klei_point["url"] in sent_links:
                valid_sent_links.append(klei_point["url"])
                continue

            role_id = data.dst_role_id_get(guild_id)
            message_header = "🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰\n+---------------------------------------------------------+\n"
            if role_id:
                message_header = f"🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰 <@&{role_id}>\n+---------------------------------------------------------+\n"
            try:
                await channel.send(
                    message_header
                    + "<:dst_icon:1101262983788769351> Open the link below :point_down::skin-tone-1: to claim **klei point** for **Don't starve together**\n"
                    + f"**Date:** {klei_point['date']}\n**Points:** {klei_point['points']}\n**Spools:** {klei_point['spools']}\n**Link:** <{klei_point['url']}>\n"
                    + "+---------------------------------------------------------+"
                )
                valid_sent_links.append(klei_point["url"])
                sent_links.append(klei_point["url"])
                data.klei_links_set(guild_id, sent_links)
            except:
                _logger.exception(
                    f"features/klei_points: Failed to send klei points ({klei_point}) "
                    + f"to the respective channel ({channel_id}) at guild ({guild_id})"
                )

        # Cleanup expired links (only keep valid sent links in the data storage)
        data.klei_links_set(guild_id, valid_sent_links)
    except:
        _logger.exception(
            f"features/klei_points: Failed to send klei points ({klei_points}) "
            + f"to the respective channel ({channel_id}) at guild ({guild_id})"
        )
