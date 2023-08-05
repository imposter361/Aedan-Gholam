from nextcord.ext import tasks
from . import check_klei_points


@tasks.loop(hours=11)
async def klei_points_task():
    await check_klei_points()
