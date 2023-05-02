from bot import *
from SteamLink import setup_on_message
from MemberJoin import setup_on_member_join
from MemberCount import setup_MemberCount, member_count
from EpicGames import setup_check_discounts,check_discounts
from KleiPoint import setup_dst
from Ready import setup_Ready
from SetRole import setup_set_role

#does logging in debug level up to critical
logging.basicConfig(filename='DiscordBot.log', filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logging.debug('Logging started ... (Here is after importing all libraries)')

async def on_ready():
    print(f"Logged in as {client.user}") # log

    setup_Ready()
    check_discounts.start()
    member_count.start()
    setup_on_message(client)
    setup_on_member_join(client)
    setup_MemberCount(client)
    setup_check_discounts(client)
    setup_dst(client)
    setup_set_role(client)

client.run(TOKEN)