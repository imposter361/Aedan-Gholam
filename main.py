import logging
import ready
import set_role
import epic_games
import steam_link
import klei_points
import member_join
import member_count
import youtube_notify
import commands
import management_commands
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
