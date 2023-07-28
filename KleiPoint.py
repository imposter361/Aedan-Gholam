import logging
import requests
import data
from bot import client
from bs4 import BeautifulSoup
from nextcord.ext import tasks


# send Klei point links in a channel.
@tasks.loop(hours=11)
async def dst():
    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        if data.get_free_games_channel_id(guild_id) == None:
            continue

        # specify the URL of the web page
        url = "https://steamcommunity.com/sharedfiles/filedetails/?id=2308653652&tscn=1639750749"

        try:
            channel = client.get_channel(data.get_free_games_channel_id(guild_id))
            # send a GET request to the URL
            response = requests.get(url)
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            row_selector = "div.bb_table_tr"
            row_elements = soup.select(row_selector)

            if row_elements:
                try:
                    for row_element in row_elements:
                        try:
                            link = (
                                str(row_element.contents[1])
                                .split("?url=")[1]
                                .split('"')[0]
                            )
                            date = (
                                str(row_element.contents[3])
                                .split("<b>")[1]
                                .split("</b>")[0]
                            )
                            points = (
                                str(row_element.contents[7]).split(">")[1].split("<")[0]
                            )
                            spools = (
                                str(row_element.contents[9]).split(">")[1].split("<")[0]
                            )

                        except:
                            continue
                        sent_links = data.get_klei_links(guild_id)
                        if link not in sent_links:
                            role_id = data.get_dst_role_id(guild_id)
                            if role_id:
                                await channel.send(
                                    f"🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰 <@&{role_id}>\n+---------------------------------------------------------+\n"
                                    + "<:dst_icon:1101262983788769351> Open the link below :point_down::skin-tone-1: to claim **klei point** for **Don't starve together**\n"
                                    + f"**Date:** {date}\n**Points:** {points}\n**Spools:** {spools}\n**Link:** <{link}>\n"
                                    + "+---------------------------------------------------------+"
                                )
                            else:
                                await channel.send(
                                    "🇳 🇪 🇼  🥹  🇱 🇮 🇳 🇰\n+---------------------------------------------------------+\n"
                                    + "<:dst_icon:1101262983788769351> Open the link below :point_down::skin-tone-1: to claim **klei point** for **Don't starve together**\n"
                                    + f"**Date:** {date}\n**Points:** {points}\n**Spools:** {spools}\n**Link:** <{link}>\n"
                                    + "+---------------------------------------------------------+"
                                )

                            sent_links.append(link)
                            data.set_klei_links(guild_id, sent_links)

                except Exception as e:
                    print(str(e) + "Exception happened in Keli")
                    logging.error(str(e) + "Exception happened in Keli")

        except Exception as e:
            print(e)
