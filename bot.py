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
ADMINS = os.getenv("ADMINS")
HOME_GUILDS = os.getenv("HOME_GUILDS")

SUBSCRIPTIONS = get_subscriptions()
