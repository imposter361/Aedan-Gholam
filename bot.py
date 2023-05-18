import os
import ast
import nextcord
from data import get_subscriptions
from dotenv import load_dotenv
from nextcord.ext import commands




intents = nextcord.Intents.all()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# SUBSCRIPTIONS = ast.literal_eval(os.getenv("SERVER_ID"))
SUBSCRIPTIONS = get_subscriptions()
ADMINS = os.getenv("ADMINS")
HOME_GUILDS = os.getenv("HOME_GUILDS")


# WELCOME_CH_ID = os.getenv("WELCOME_CH_ID")

MEMBER_COUNT_CH_ID = os.getenv("MEMBER_COUNT_CH_ID")
EPIC_CHANNEL_ID = os.getenv("EPIC_CHANNEL_ID")
GAMES_FILE = os.getenv("GAMES_FILE")  # games.txt
KLEI_LINKS_FILE = os.getenv("KLEI_LINKS_FILE")  # KleiLinks.txt
SET_ROLE_MESSAGE_ID = os.getenv("SET_ROLE_MESSAGE_ID")
