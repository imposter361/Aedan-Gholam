from . import check_free_games
from nextcord.ext import tasks


@tasks.loop(minutes=55)
async def epic_games_task():
    await check_free_games()
