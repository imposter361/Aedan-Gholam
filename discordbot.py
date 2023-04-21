import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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
    if user_message.startswith(steam_store) or user_message.startswith(steam_community):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}sent a steam link. \nOpen in browser: \
                                       \n{user_message} \nOpen in Steam: \nsteam://openurl/{user_message}")
            
        except Exception as e:
            print(e)


client.run(TOKEN)




