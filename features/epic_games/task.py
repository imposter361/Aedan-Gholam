import logging
from . import is_active, check_free_games
from nextcord.ext import tasks

_logger = logging.getLogger("main")


@tasks.loop(minutes=55)
async def epic_games_task():
    if not is_active():
        return

    _logger.debug("features/epic_games: Running free Epic Games task...")
    await check_free_games()
