import os
import json
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands


intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMINS = json.loads(os.getenv("ADMINS"))
HOME_GUILDS = json.loads(os.getenv("HOME_GUILDS"))
