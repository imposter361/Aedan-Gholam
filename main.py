import events
import features
import commands

import logging
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
