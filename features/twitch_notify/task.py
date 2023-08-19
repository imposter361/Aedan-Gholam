from . import check_for_twitch_live
from nextcord.ext import tasks


@tasks.loop(minutes=1)
async def twitch_notify_task():
    await check_for_twitch_live()
