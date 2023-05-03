from urlextract import URLExtract
import discord
from bot import *


lock = asyncio.Lock()

#on_message
@client.event
async def on_message(message):
    ## !m.delete message added
    lower_message = str(message.content).lower()
    if lower_message.startswith('!m.delete'):
        roles_to_check = ["dev-team"]
        if any(role.name in roles_to_check for role in message.author.roles):
            try:
                num_messages = int(message.content.split(' ')[1])
                await message.channel.purge(limit=num_messages + 1)
                if num_messages == 1:
                    sent_message = await message.channel.send(f'{num_messages} message deleted.')
                else:
                    sent_message = await message.channel.send(f'{num_messages} messages have been deleted.')
                await asyncio.sleep(4)
                await sent_message.delete()
                #await message.channel.delete(limit= 1)
            except Exception as e:
                print(str(e) + "Exception happend in message delete.")

    #gholam command added (auto reply)
    if ("gholam") in lower_message:
        if message.author != client.user:
            await message.reply(f"Gholametam v{Bot_version}")


#add "steam://openurl/" at the beginning of steam links.
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' in channel: ({channel})") # log

    steam_store = "https://store.steampowered.com"
    steam_community = "https://steamcommunity.com"

    extractor = URLExtract()
    message_urls = extractor.find_urls(f"{user_message}")

    all_start_with_steam = all(item.startswith(
        'steam://openurl/') for item in message_urls)

    steam_links = []
    if all_start_with_steam:
        return
    else:
        for i in message_urls:
            if i.startswith(steam_store) or i.startswith(steam_community):
                steam_links.append(f"steam://openurl/{i}\n")

    if steam_store in user_message or steam_community in user_message:
        try:
            # Check if the server has an active subscription or not
            if str(message.guild.id) in SUBSCRIPTIONS and SUBSCRIPTIONS[str(message.guild.id)]:
                URL = ''.join(steam_links)
                embed = discord.Embed(description= URL)
                await message.reply(f" Open directly in  <:steam_icon:1099351469674729553> " , embed = embed)

        except Exception as e:
            print(str(e) + "Exception happened in Stemlink edition") # log

def setup_on_message(bot):
    bot.event(on_message)           