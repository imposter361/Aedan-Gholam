import logging
from bot import client
from version import VERSION
from KleiPoint import dst
from MemberCount import member_count
from EpicGames import check_discounts


@client.event
async def on_ready():
    check_discounts.start()
    dst.start()
    member_count.start()
    username = str(client.user).split("#")[0]
    print(f"Logged in as {username} v{VERSION}")
    logging.info(f"Logged in as {username} v{VERSION}")
