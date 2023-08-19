import os
import json
import logging
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

_logger = logging.getLogger("main")

_intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="!", intents=_intents)


_logger.debug("bot: Loading .env file...")
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMINS = json.loads(os.getenv("ADMINS"))
HOME_GUILDS = json.loads(os.getenv("HOME_GUILDS"))
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
