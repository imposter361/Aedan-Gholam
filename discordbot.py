import os
import discord
from dotenv import load_dotenv
from urlextract import URLExtract

load_dotenv()
TOKEN = os.getenv('TESTBOT_TOKEN')

int = discord.Intents.default()
int.message_content = True

client = discord.Client(intents = int)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' in channel: ({channel})")
    
    steam_store = "https://store.steampowered.com"
    steam_community = "https://steamcommunity.com"

    extractor = URLExtract()
    UM = extractor.find_urls(f"{user_message}")
    URL = ''.join(UM)
    URL = URL.replace("'", "")

    if steam_store in user_message or steam_community in user_message:
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}sent a steam link and said: \
                                       \n{user_message} \n\n<:steam:1099147813381746739> Open in Steam directly: \nsteam://openurl/{URL}")
        except Exception as e:
            print(e)
  
client.run(TOKEN)




