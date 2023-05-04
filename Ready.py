from bot import *
from KleiPoint import dst
from MemberCount import member_count
from EpicGames import check_discounts

@client.event
async def on_ready():
    check_discounts.start()
    dst.start()
    member_count.start()
    username = str(client.user).split('#')[0]
    print(f"Logged in as {username} v{Bot_version}")
    logging.info(f"Logged in as {username} v{Bot_version}")


def setup_Ready(bot):
    bot.event(on_ready)