import data
from bot import client
from youtubesearchpython import Playlist, playlist_from_channel_id


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    from . import task


async def check_for_new_youtube_video():
    if not _active:
        return False

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue

        rules = data.get_yt_notif_rules(guild_id)
        if not rules:
            continue

        for yt_channel_id in rules:
            try:
                last_video = get_last_video_of_youtube_channel(yt_channel_id)
                if rules[yt_channel_id]["last_video_id"] != last_video["id"]:
                    # send message
                    discord_channel = client.get_channel(
                        rules[yt_channel_id]["discord_channel_id"]
                    )
                    await discord_channel.send(
                        f"A new video from **{last_video['channel_name']}**:point_down_tone1:"
                        + f"\nhttps://www.youtube.com/watch?v={last_video['id']}"
                    )
                    # update stored last video id
                    data.set_yt_last_video_id(guild_id, yt_channel_id, last_video["id"])
            except Exception as e:
                print(e)


def get_last_video_of_youtube_channel(yt_channel_id):
    playlist = Playlist(playlist_from_channel_id(yt_channel_id))
    video = playlist.videos[0]
    return {
        "id": video["id"],
        "channel_name": video["channel"]["name"],
    }
