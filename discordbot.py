import os
import discord
from dotenv import load_dotenv
from urlextract import URLExtract
import ast

load_dotenv()
TOKEN = os.getenv('TESTBOT_TOKEN')
WELCOME_CH = os.getenv('WELCOME_CH')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents = intents)

# Servers allowed or disallowed
subscriptions = ast.literal_eval(os.getenv('SERVER_ID'))

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

    if steam_store in user_message or steam_community in user_message:

        try:
            # Check if the server has an active subscription or not
            if str(message.guild.id) in subscriptions and subscriptions[str(message.guild.id)]:
                await message.delete()
                URL = ''.join(slink)
                await message.channel.send(f"{message.author.mention} sent a steam link.\
                                       \n<:chrome:1099349401501188128> {user_message} \n\n<:steam:1099147813381746739> Open in Steam directly:\n{URL}")
            else:
                return
        
        except Exception as e:
            print(e)

@client.event 
async def on_member_join(member):
    
    guild = member.guild
    channel = client.get_channel(int(WELCOME_CH))
    author_profile_pic = member.avatar
    embed = discord.Embed() 
    embed.set_image(url=author_profile_pic)
    await channel.send(f"Salam {member.mention} be **{guild}** khosh oomadi!\n", embed=embed)
    
client.run(TOKEN)