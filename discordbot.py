import os
import discord
import ast
import requests
from dotenv import load_dotenv
from urlextract import URLExtract
from discord.ext import commands, tasks
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CH = os.getenv('WELCOME_CH')
MEMBER_COUNT_CH = os.getenv('MEMBER_COUNT_CH')
EPIC_CHANNEL = os.getenv('EPIC_CHANNEL')
GAMES_FILE = os.getenv('GAMES_FILE') #games.txt
ROLE_MESSAGE = os.getenv('ROLE_MESSAGE')

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Servers allowed or disallowed
subscriptions = ast.literal_eval(os.getenv('SERVER_ID'))

@client.event
async def on_ready():
    check_discounts.start()
    print(f"Logged in as {client.user}")

# add "steam://openurl/" at the beginning of steam links.
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
            if str(message.guild.id) in subscriptions and subscriptions[str(message.guild.id)]:
                URL = ''.join(steam_links)
                embed = discord.Embed(description= URL)
                await message.reply(f" Open directly in  <:steam_icon:1099351469674729553> " , embed = embed)

        except Exception as e:
            print(e)

# send welcome message for new members:
@client.event
async def on_member_join(member):
    if str(member.guild.id) in subscriptions and subscriptions[str(member.guild.id)]:
        guild = member.guild
        channel = client.get_channel(int(WELCOME_CH))
        author_profile_pic = member.avatar
        embed = discord.Embed()
        embed.set_image(url=author_profile_pic)
        await channel.send(f"Salam {member.mention} be **{guild}** khosh oomadi!\n", embed=embed)
        # Update member count on join
        members_count_channel = client.get_channel(int(MEMBER_COUNT_CH))
        name = "Total members: " + str(guild.member_count)
        await members_count_channel.edit(name=name)

# Update member count on leave
@client.event
async def on_member_remove(member):
    if str(member.guild.id) in subscriptions and subscriptions[str(member.guild.id)]:
        members_count_channel = client.get_channel(int(MEMBER_COUNT_CH))
        guild = member.guild
        name = "Total members: " + str(guild.member_count)
        await members_count_channel.edit(name=name)

# Run the task every 12 hours
@tasks.loop(hours=12)  
async def check_discounts():
    await client.wait_until_ready()
    channel = client.get_channel(int(EPIC_CHANNEL))
    # Make a request to the Epic Games
    response = requests.get(f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US&' \
                            f'spaceId=1af6c7f8a3624b1788eaf23175fdd16f&' \
                            f'redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fstore%2Fen-US%2F&' \
                            f'key=da1563f4abe7480fb43364b7d30d9a7b&' \
                            f'promoId=freegames')
    response_json = response.json()

    # Find all the games that are currently free
    for game in response_json['data']['Catalog']['searchStore']['elements']:
        if game['price']['totalPrice']['discountPrice'] == 0:
            try:
                end_date = datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if game['productSlug'] and ['title']:
                    end_date_str = end_date.strftime('%b %d, %Y')
                    game_name = game['title']
                    game_link = f"https://launcher.store.epicgames.com/en-US/p/{game['productSlug']}"
                    with open(GAMES_FILE, "a+") as file:
                        file.seek(0)
                        sent_games = [line.strip() for line in file.readlines()]
                        file.close()
                    if game_name not in sent_games:
                        message = "The following game is currently available for free on the Epic Games Store:\n"
                        await channel.send(f"\n {message}\n* **{game_name}** - (ends {end_date_str})\n{game_link}\n")
                        with open(GAMES_FILE, "a") as file:
                            file.write(game_name + "\n")
            except Exception as e:
                print(e)

#add or remove roles by reactions
global reactions
reactions = {'csgo_icon':'CSGO',
            'minecraft_icon':'Minecraft',
            'valorant_icon':'Valorant',
            'r6_icon':'R6',
            'warzon_icon':'Warzone',
            'dst_icon':'Don\'t starve together' ,
            'dota2_icon':'Dota 2',
            'pubg_icon':'Pubg',
            'epic_icon':'Bounty Hunter',
            'amongus_icon':'Amongus',
            'fortnite_icon':'Fortnite',
            
            }

# Add roles
@client.event
async def on_raw_reaction_add(role_set):
    guild = discord.utils.find(lambda g: g.id == role_set.guild_id, client.guilds)
    reaction = role_set.emoji.name

    if reaction in reactions.keys() and role_set.message_id == int(ROLE_MESSAGE):
        role = discord.utils.get(guild.roles, name= reactions.get(reaction))
        if role is not None:
            member = discord.utils.find(lambda m: m.id == role_set.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f"Role {role} added to {member}")
  
# Remove roles
@client.event
async def on_raw_reaction_remove(role_unset):
    guild = discord.utils.find(lambda g: g.id == role_unset.guild_id, client.guilds)
    reaction = role_unset.emoji.name
    
    if reaction in reactions.keys() and role_unset.message_id == int(ROLE_MESSAGE):
        role = discord.utils.get(guild.roles, name = reactions.get(reaction))
        if role is not None:
            member = discord.utils.find(lambda m: m.id == role_unset.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"Role {role} removed from {member}")
                
client.run(TOKEN)
