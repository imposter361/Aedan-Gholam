import data
import logging
from bot import client
from features.epic_games.task import epic_games_task
from features.klei_points.task import klei_points_task
from features.member_count.task import member_count_task
from features.youtube_notify.task import youtube_notify_task
from version import VERSION

_logger = logging.getLogger("main")


@client.event
async def on_ready():
    bot_username = str(client.user).split("#")[0]
    _logger.info(f"events/ready: Logged in as {bot_username} v{VERSION}")

    await data.check_for_data_migrations()
    data.backup()

    # Features' first run:
    epic_games_task.start()
    klei_points_task.start()
    member_count_task.start()
    youtube_notify_task.start()

    _logger.info("events/ready: Initial tasks have been started!")
