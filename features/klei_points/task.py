import logging
from . import is_active, check_klei_points_for_all_guilds
from nextcord.ext import tasks

_logger = logging.getLogger("main")


@tasks.loop(minutes=57)
async def klei_points_task():
    if not is_active():
        return

    _logger.debug("features/klei_points: Running free Klei points task...")
    await check_klei_points_for_all_guilds()
