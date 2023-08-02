import logging
from bot import client
from version import VERSION
from KleiPoint import dst
from MemberCount import member_count
from EpicGames import check_discounts
from youtube_notify import check_for_new_youtube_video


@client.event
async def on_ready():
    check_discounts.start()
    dst.start()
    check_for_new_youtube_video.start()
    member_count.start()
    username = str(client.user).split("#")[0]
    print(f"Logged in as {username} v{VERSION}")
    logging.info(f"Logged in as {username} v{VERSION}")
