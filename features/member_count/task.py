import logging
from . import is_active, update_member_count_for_all_guilds
from nextcord.ext import tasks

_logger = logging.getLogger("main")


@tasks.loop(minutes=11)
async def member_count_task():
    if not is_active():
        return

    _logger.debug("features/member_count: Running member count updater task...")
    await update_member_count_for_all_guilds()
