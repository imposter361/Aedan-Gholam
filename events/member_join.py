from bot import client
from features.welcome_banner import send_welcome_banner


@client.event
async def on_member_join(member):
    await send_welcome_banner(member)
