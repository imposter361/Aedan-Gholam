from bot import *

# send Klei point links in a channel.
@tasks.loop(hours=12)
async def dst():
    # specify the URL of the web page
    url = 'https://steamcommunity.com/sharedfiles/filedetails/?id=2308653652&tscn=1639750749'
    channel = client.get_channel(int(EPIC_CHANNEL))
    # send a GET request to the URL
    response = requests.get(url)
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    link_selector = 'a.bb_link[href*="https://accounts.klei.com/link/"]'
    link_elements = soup.select(link_selector)
    if link_elements:
        try:
            for link_element in link_elements:
                link = link_element['href'].split("=")
                link = link.pop(1)
                with open(KLEI_LINKS, "a+") as file:
                    file.seek(0)
                    sent_link = [line.strip() for line in file.readlines()]
                    file.close()
                if link not in sent_link:
                    await channel.send(f"<@&1101266966771155015>\n<:dst_icon:1101262983788769351> open this link to claim **klei point** for **Don't starve together**:\n<{link}>")
                    with open(KLEI_LINKS, "a") as file:
                        file.write(link + "\n")
        except Exception as e:
            print(str(e) + "Exception happened in Keli")
            logging.error(str(e) + "Exception happened in Keli")

def setup_dst(bot):
    bot.event(dst)