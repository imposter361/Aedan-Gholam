from bot import *
from SteamLink import setup_on_message
from MemberJoin import setup_on_member_join
from MemberCount import setup_MemberCount, member_count
from EpicGames import setup_check_discounts,check_discounts
from KleiPoint import setup_dst
from Ready import setup_Ready
from SetRole import setup_set_role
from Commands import setup_Commands

#does logging in debug level up to critical
logging.basicConfig(filename='DiscordBot.log', filemode='a',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info('Logging started ... (Here is after importing all libraries)')

client.run(TOKEN)