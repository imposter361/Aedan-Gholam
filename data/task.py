from . import backup
from nextcord.ext import tasks


@tasks.loop(hours=12)
async def backup_data_task():
    backup()
