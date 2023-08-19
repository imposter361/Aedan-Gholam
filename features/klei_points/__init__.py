import data
import logging
import requests
from bot import client
from bs4 import BeautifulSoup

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'klei_points'")
    from . import task


# Check for free klei points then send them in the chat.
async def check_klei_points():
    if not _active:
        return False

    _logger.debug("features/klei_points: Running free Klei points task...")

    klei_points = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.get_klei_links_channel_id(guild_id)
        if not channel_id:
            continue

        if not klei_points:
            klei_points = _get_klei_points()

        await _send_klei_points_for_guild(guild_id, channel_id, klei_points)


def _get_klei_points():
    _logger.debug("features/klei_points: Getting free Klei points list...")
    klei_points = []
    # get links just for the first time
    url = "https://steamcommunity.com/sharedfiles/filedetails/?id=2308653652&tscn=1639750749"

    try:
        response = requests.get(url)
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        row_selector = "div.bb_table_tr"
        row_elements = soup.select(row_selector)

        if not row_elements:
            return klei_points

        try:
            for row_element in row_elements:
                if "Outdated" in str(row_element.contents[1]):
                    continue
                try:
                    klei_points.append(
                        {
                            "url": (
                                str(row_element.contents[1])
                                .split("?url=")[1]
                                .split('"')[0]
                            ),
                            "date": (
                                str(row_element.contents[3])
                                .split("<b>")[1]
                                .split("</b>")[0]
                            ),
                            "points": (
                                str(row_element.contents[7]).split(">")[1].split("<")[0]
                            ),
                            "spools": (
                                str(row_element.contents[9]).split(">")[1].split("<")[0]
                            ),
                        }
                    )
                except:
                    continue

        except:
            _logger.exception(
                "features/klei_points: Could not process free klei points links."
            )

    except:
        _logger.exception("features/klei_points: Could not get free klei points links.")

    return klei_points


async def _send_klei_points_for_guild(guild_id, channel_id, klei_points):
    try:
        channel = client.get_channel(channel_id)
        sent_links = data.get_klei_links(guild_id)
        valid_sent_links = []

        for klei_point in klei_points:
            if klei_point["url"] in sent_links:
                valid_sent_links.append(klei_point["url"])
                continue

            role_id = data.get_dst_role_id(guild_id)
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
                data.set_klei_links(guild_id, sent_links)
            except:
                _logger.exception(
                    f"features/klei_points: Failed to send klei points ({klei_point}) "
                    + f"to the respective channel ({channel_id}) at guild ({guild_id})"
                )

        # Cleanup expired links (only keep valid sent links in the data storage)
        data.set_klei_links(guild_id, valid_sent_links)
    except:
        _logger.exception(
            f"features/klei_points: Failed to send klei points ({klei_points}) "
            + f"to the respective channel ({channel_id}) at guild ({guild_id})"
        )
