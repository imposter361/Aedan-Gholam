import os
import discord
from dotenv import load_dotenv
from urlextract import URLExtract
import ast

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CH = os.getenv('WELCOME_CH')
MEMBER_COUNT_CH = os.getenv('MEMBER_COUNT_CH')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Servers allowed or disallowed
subscriptions = ast.literal_eval(os.getenv('SERVER_ID'))

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
                steam_links.append(f"steam://openurl/<{i}>\n")

    if steam_store in user_message or steam_community in user_message:
        try:
            # Check if the server has an active subscription or not
            if str(message.guild.id) in subscriptions and subscriptions[str(message.guild.id)]:
                URL = ''.join(steam_links)
                await message.reply(f"<:steam_icon:1099351469674729553> Open directly in steam: \n{URL}")

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


client.run(TOKEN)
