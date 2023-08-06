from nextcord.ext import tasks
from . import update_member_count


@tasks.loop(minutes=11)
async def member_count_task():
    await update_member_count()
