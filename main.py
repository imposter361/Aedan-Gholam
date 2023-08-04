import logging
import events.ready
import events.member_join
import features.set_role
import features.epic_games
import features.steam_link
import features.klei_points
import features.member_count
import features.youtube_notify
import commands.commands
import commands.management_commands
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
