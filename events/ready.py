import logging
from bot import client
from version import VERSION
from features.klei_points import dst
from features.member_count import member_count
from features.epic_games import check_discounts
from features.youtube_notify import check_for_new_youtube_video


@client.event
async def on_ready():
    check_discounts.start()
    dst.start()
    check_for_new_youtube_video.start()
    member_count.start()
    username = str(client.user).split("#")[0]
    print(f"Logged in as {username} v{VERSION}")
    logging.info(f"Logged in as {username} v{VERSION}")
