import logging
from bot import client
from version import VERSION
from features.epic_games.task import epic_games_task
from features.klei_points.task import klei_points_task
from features.member_count.task import member_count_task
from features.youtube_notify.task import youtube_notify_task


@client.event
async def on_ready():
    bot_username = str(client.user).split("#")[0]
    print(f"Logged in as {bot_username} v{VERSION}")
    logging.info(f"Logged in as {bot_username} v{VERSION}")

    # Features' first run:
    epic_games_task.start()
    klei_points_task.start()
    member_count_task.start()
    youtube_notify_task.start()

    print("Starting tasks have started!")
