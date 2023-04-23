import os
import discord
from dotenv import load_dotenv
from urlextract import URLExtract

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
<<<<<<< HEAD
    
    all_start_with_steam = all(item.startswith('steam://openurl/') for item in UM)

    slink = []
    if all_start_with_steam:
        return
    else:
        for i in UM :
            if i.startswith(steam_store):
                slink.append(f"steam://openurl/{i}\n")
            elif i.startswith(steam_community):
                slink.append(f"steam://openurl/{i}\n")
            else:
                continue
=======
    URL = ''.join(UM)
    URL = URL.replace("'", "")
    
    if user_message.startswith(steam_store) or user_message.startswith(steam_community):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}sent a steam link. \nOpen in browser: \
                                       \n{user_message} \n\n<:steam:1099147813381746739> Open in Steam: \nsteam://openurl/{user_message}")
            
        except Exception as e:
            print(e)
>>>>>>> b390d0879f4583f4bd87f8f974c10d0ec98e06c0

    elif steam_store in user_message or steam_community in user_message:
        try:
            await message.delete()
<<<<<<< HEAD
            URL = ''.join(slink)
            await message.channel.send(f"{message.author.mention} sent a steam link.\
                                   \n<:chrome:1099349401501188128> {user_message} \n\n<:steam:1099147813381746739> Open in Steam directly:\n{URL}")
        except Exception as e:
            print(e)
client.run(TOKEN)
=======
            await message.channel.send(f"{message.author.mention}sent a steam link and said: \
                                       \n{user_message} \n\n<:steam:1099147813381746739> Open in Steam: \nsteam://openurl/{URL}")
        except Exception as e:
            print(e)
  
client.run(TOKEN)
>>>>>>> b390d0879f4583f4bd87f8f974c10d0ec98e06c0
