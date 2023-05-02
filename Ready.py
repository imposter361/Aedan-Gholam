from bot import *
from KleiPoint import dst
from MemberCount import member_count
from EpicGames import check_discounts

@client.event
async def on_ready():
    check_discounts.start()
    dst.start()
    member_count.start()
    print(f"Logged in as {client.user}") # log



def setup_Ready(bot):
    bot.event(on_ready)