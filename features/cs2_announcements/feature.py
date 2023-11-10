import data
import json
import logging
import re
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

    last_announcement_time = None
    last_announcement_link = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.cs2_announcements_channel_id_get(guild_id)
        if not channel_id:
            continue

        if not last_announcement_time:
            (
                last_announcement_time,
                last_announcement_link,
            ) = await _get_last_cs2_announcement()
            if not last_announcement_time or not last_announcement_link:
                _logger.warning(
                    "features/cs2_announcements: No valid CS2 announcement was found."
                )
                break

        last_sent_announcement_time = (
            data.cs2_announcements_last_sent_announcement_time_get(guild_id)
        )
        if (
            last_sent_announcement_time
            and last_sent_announcement_time >= last_announcement_time
        ):
            continue

        await _send_cs2_announcement_for_guild(
            guild_id, channel_id, last_announcement_time, last_announcement_link
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
        last_announcement_time,
        last_announcement_link,
    ) = await _get_last_cs2_announcement()

    if not last_announcement_time or not last_announcement_link:
        return

    last_sent_announcement_time = (
        data.cs2_announcements_last_sent_announcement_time_get(guild_id)
    )
    if (
        last_sent_announcement_time
        and last_sent_announcement_time >= last_announcement_time
    ):
        return

    await _send_cs2_announcement_for_guild(
        guild_id, channel_id, last_announcement_time, last_announcement_link
    )


async def _get_last_cs2_announcement():
    _logger.debug("features/cs2_announcements: Getting last CS2 announcement...")

    last_announcement_time = None
    last_announcement_link = None

    try:
        url = "https://steamcommunity.com/games/CSGO/announcements/"
        response = await aiohttp_get(url)
        soup = BeautifulSoup(response, "html.parser")
        element = soup.find("div", {"data-partnereventstore": re.compile(r".*")})
        data = json.loads(element.attrs["data-partnereventstore"])
        last_announcement_time = data[0]["announcement_body"]["posttime"]
        announcement_gid = data[0]["announcement_body"]["gid"]
        last_announcement_link = (
            "https://steamcommunity.com/games/CSGO/announcements/detail/"
            + announcement_gid
        )
    except:
        _logger.exception(
            "features/cs2_announcements: Could not get last CS2 announcement."
        )

    return last_announcement_time, last_announcement_link


async def _send_cs2_announcement_for_guild(
    guild_id, channel_id, announcement_time, announcement_link
):
    try:
        discord_channel = client.get_channel(channel_id)
        if not discord_channel:
            _logger.debug(
                "features/cs2_announcements: Failed to get channel with id of: "
                + f"{channel_id} in guild: {guild_id}"
            )
            return

        message = f"A new [**CS2 announcement**]({announcement_link}) has published!"
        role_id = data.cs2_role_id_get(guild_id)
        role_mention = ""
        if role_id:
            role_mention = f"<@&{role_id}>\n"
        await discord_channel.send(f"{message} {role_mention}")
        _logger.debug(
            f"features/cs2_announcements: Sent a CS2 announcement. "
            + f"announcement_link: '{announcement_link}' announcement_time: '{announcement_time}' "
            + f" channel: '{discord_channel.name}' ({discord_channel.id}) "
            + f" guild: '{discord_channel.guild.name}' ({discord_channel.guild.id})"
        )
        data.cs2_announcements_last_sent_announcement_time_set(
            guild_id, announcement_time
        )
    except:
        _logger.exception(
            f"features/cs2_announcements: Failed to send CS2 announcement ({announcement_link}) "
            + f"to the respective channel ({channel_id}) at guild ({guild_id})"
        )
