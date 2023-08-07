from bot import client
from features.welcome_banner import send_welcome_banner
from nextcord import Member


@client.event
async def on_member_join(member: Member):
    await send_welcome_banner(member)
