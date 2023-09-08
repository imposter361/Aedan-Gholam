import data
import logging
from bot import client
from youtubesearchpython import Playlist, playlist_from_channel_id


_logger = logging.getLogger("main")

if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'youtube_notify'")
    from . import task


async def check_for_new_youtube_video():
    if not _active:
        return False

    channels_last_videos = {}

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        rules = data.yt_notif_rules_get(guild_id)
        if not rules:
            continue

        for yt_channel_id in rules:
            try:
                if yt_channel_id not in channels_last_videos:
                    last_video = get_last_video_of_youtube_channel(yt_channel_id)
                    channels_last_videos[yt_channel_id] = last_video

                last_video = channels_last_videos[yt_channel_id]
                if rules[yt_channel_id]["last_video_id"] != last_video["id"]:
                    # send message
                    discord_channel = client.get_channel(
                        rules[yt_channel_id]["discord_channel_id"]
                    )
                    if not discord_channel:
                        _logger.debug(
                            "features/youtube_notify: Failed to get channel with id of: "
                            + f"{rules[yt_channel_id]['discord_channel_id']} in guild: {guild_id}"
                        )
                        return

                    message = f"A new video from **{last_video['channel_name']}**:point_down_tone1:"
                    if rules[yt_channel_id].get("custom_text_message"):
                        message = rules[yt_channel_id]["custom_text_message"]
                    if "\\n" in message:
                        message = message.replace("\\n", "\n")
                    message = (
                        message
                        + f"\nhttps://www.youtube.com/watch?v={last_video['id']}"
                    )
                    await discord_channel.send(message)
                    _logger.debug(
                        f"features/youtube_notify: Sent a youtube video notification. "
                        + f"video_id: '{last_video['id']}' yt_channel: '{last_video['channel_name']}' "
                        + f" channel: '{discord_channel.name}' ({discord_channel.id}) "
                        + f" guild: '{discord_channel.guild.name}' ({discord_channel.guild.id}) "
                    )
                    # update stored last video id
                    data.yt_last_video_id_set(
                        guild_id,
                        yt_channel_id,
                        last_video["channel_name"],
                        last_video["id"],
                    )
            except:
                _logger.exception(
                    "features/youtube_notify: Failed to process possible "
                    + f"new video notification for channel id '{yt_channel_id}'"
                )


def get_last_video_of_youtube_channel(yt_channel_id):
    _logger.debug(
        "features/youtube_notify: Getting the most recent Youtube video "
        + f"with channel id of '{yt_channel_id}'"
    )
    playlist = Playlist(playlist_from_channel_id(yt_channel_id))
    video = playlist.videos[0]
    return {
        "id": video["id"],
        "channel_name": video["channel"]["name"],
    }
