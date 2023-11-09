import logging
from . import is_active, check_cs2_announcements_for_all_guilds
from nextcord.ext import tasks

_logger = logging.getLogger("main")


@tasks.loop(minutes=54)
async def cs2_announcements_task():
    if not is_active():
        return

    _logger.debug("features/cs2_announcements: Running CS2 announcements task...")
    await check_cs2_announcements_for_all_guilds()
