import os
import nextcord
import ast
import requests
import logging
import asyncio
import random
import subprocess
import re
from typing import Optional
from dotenv import load_dotenv
from urlextract import URLExtract
from nextcord import Interaction, SlashOption, FFmpegPCMAudio
from nextcord.ext import commands, tasks
from datetime import datetime
from bs4 import BeautifulSoup


intents = nextcord.Intents.all()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix= '!', intents=intents)

load_dotenv()
SUBSCRIPTIONS = ast.literal_eval(os.getenv('SERVER_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CH_ID = os.getenv('WELCOME_CH_ID')
MEMBER_COUNT_CH_ID = os.getenv('MEMBER_COUNT_CH_ID')
EPIC_CHANNEL_ID = os.getenv('EPIC_CHANNEL_ID')
GAMES_FILE = os.getenv('GAMES_FILE') #games.txt
KLEI_LINKS_FILE = os.getenv('KLEI_LINKS_FILE') #KleiLinks.txt
SET_ROLE_MESSAGE_ID = os.getenv('SET_ROLE_MESSAGE_ID')

Bot_version = "0.5"