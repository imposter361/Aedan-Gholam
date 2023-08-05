import data
import logging
import requests
from bot import client
from bs4 import BeautifulSoup


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    from . import task


# Check for free klei points then send them in the chat.
async def check_klei_points():
    if not _active:
        return False

    links = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.get_free_games_channel_id(guild_id)
        if not channel_id:
            continue

        if not links:
            links = _get_klei_links()

        await _send_klei_links_for_guild(guild_id, channel_id, links)


def _get_klei_links():
    links = []
    # get links just for the first time
    url = "https://steamcommunity.com/sharedfiles/filedetails/?id=2308653652&tscn=1639750749"

    try:
        response = requests.get(url)
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        row_selector = "div.bb_table_tr"
        row_elements = soup.select(row_selector)

        if not row_elements:
            return links

        try:
            for row_element in row_elements:
                if "Outdated" in str(row_element.contents[1]):
                    continue
                try:
                    links.append(
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

        except Exception as e:
            print(str(e) + "Exception happened in Keli")
            logging.error(str(e) + "Exception happened in Keli")

    except Exception as e:
        print(e)

    return links


async def _send_klei_links_for_guild(guild_id, channel_id, links):
    channel = client.get_channel(channel_id)
    sent_links = data.get_klei_links(guild_id)

    for link in links:
        if link["url"] in sent_links:
            continue

        role_id = data.get_dst_role_id(guild_id)

        message_header = "🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰\n+---------------------------------------------------------+\n"
        if role_id:
            message_header = f"🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰 <@&{role_id}>\n+---------------------------------------------------------+\n"
        await channel.send(
            message_header
            + "<:dst_icon:1101262983788769351> Open the link below :point_down::skin-tone-1: to claim **klei point** for **Don't starve together**\n"
            + f"**Date:** {link['date']}\n**Points:** {link['points']}\n**Spools:** {link['spools']}\n**Link:** <{link['url']}>\n"
            + "+---------------------------------------------------------+"
        )
        sent_links.append(link)
        data.set_klei_links(guild_id, sent_links)
