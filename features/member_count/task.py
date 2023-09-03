from . import update_all_member_counts
from nextcord.ext import tasks


@tasks.loop(minutes=11)
async def member_count_task():
    await update_all_member_counts()
