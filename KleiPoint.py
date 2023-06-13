import logging
import requests
from bot import client
from data import (
    get_free_games_channel_id,
    set_klei_links,
    get_klei_links,
    get_subscriptions,
)
from bs4 import BeautifulSoup
from nextcord.ext import tasks


# send Klei point links in a channel.
@tasks.loop(hours=12)
async def dst():
    
    subscriptions = get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        if get_free_games_channel_id(guild_id) == None:
            continue

        
        # specify the URL of the web page
        url = "https://steamcommunity.com/sharedfiles/filedetails/?id=2308653652&tscn=1639750749"
        
        try:
            channel = client.get_channel(get_free_games_channel_id(guild_id))
            # send a GET request to the URL
            response = requests.get(url)
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            link_selector = 'a.bb_link[href*="https://accounts.klei.com/link/"]'
            link_elements = soup.select(link_selector)
            if link_elements:
                try:
                    for link_element in link_elements:
                        link = link_element["href"].split("=")
                        link = link.pop(1)

                        sent_links = get_klei_links(guild_id)
                        if link not in sent_links:
                            await channel.send(
                                f"<@&1101266966771155015>\n<:dst_icon:1101262983788769351> open this link to claim **klei point** for **Don't starve together**:\n<{link}>"
                            )
                            sent_links.append(link)
                            set_klei_links(guild_id, sent_links)

                except Exception as e:
                    print(str(e) + "Exception happened in Keli")
                    logging.error(str(e) + "Exception happened in Keli")
                    
        except Exception as e:
            print(e)
