from nextcord.ext import tasks
from . import check_free_games


@tasks.loop(hours=12)
async def epic_games_task():
    await check_free_games()
