import data
import googleapiclient.discovery
from bot import client, YOUTUBE_API_KEY
from nextcord.ext import tasks


@tasks.loop(minutes=10)
async def check_for_new_youtube_video():
    subscriptions = data.get_subscriptions()

    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue

        rules = data.get_yt_notif_rules(guild_id)
        if not rules:
            continue

        for yt_channel_id in rules:
            try:
                last_video_id = get_last_video_id_of_youtube_channel(yt_channel_id)
                if rules[yt_channel_id]["last_video_id"] != last_video_id:
                    # send message
                    discord_channel = client.get_channel(
                        rules[yt_channel_id]["discord_channel_id"]
                    )
                    await discord_channel.send(
                        f"https://www.youtube.com/watch?v={last_video_id}"
                    )
                    # update stored last video id
                    data.set_yt_last_video_id(guild_id, yt_channel_id, last_video_id)
            except Exception as e:
                print(e)


def get_last_video_id_of_youtube_channel(yt_channel_id):
    youtube_api = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY
    )

    # Get the latest video from the channel
    channel_videos = (
        youtube_api.search()
        .list(
            part="snippet",
            channelId=yt_channel_id,
            type="video",
            order="date",
            maxResults=1,
        )
        .execute()
    )

    latest_video_id = channel_videos["items"][0]["id"]["videoId"]

    return latest_video_id
