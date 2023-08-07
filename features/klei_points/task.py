from . import check_klei_points
from nextcord.ext import tasks


@tasks.loop(hours=11)
async def klei_points_task():
    await check_klei_points()
