import logging
from . import is_active, check_new_youtube_videos_for_all_guilds
from nextcord.ext import tasks

_logger = logging.getLogger("main")


@tasks.loop(minutes=15)
async def youtube_notify_task():
    if not is_active():
        return

    _logger.debug("features/youtube_notify: Running Youtube notify task...")
    await check_new_youtube_videos_for_all_guilds()
