from . import update_member_count
from nextcord.ext import tasks


@tasks.loop(minutes=11)
async def member_count_task():
    await update_member_count()
