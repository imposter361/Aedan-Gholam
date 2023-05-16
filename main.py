import logging
import SteamLink
import MemberJoin
import MemberCount
import EpicGames
import KleiPoint
import Ready
import SetRole
import Commands
from bot import client, TOKEN

# does logging in debug level up to critical
logging.basicConfig(
    filename="DiscordBot.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)
logging.info("Logging started ... (Here is after importing all libraries)")

client.run(TOKEN)
