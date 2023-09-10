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


_MAX_RECENT_VIDEOS = 5


async def check_new_youtube_videos_for_all_guilds():
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
                    videos = _get_recent_videos_of_youtube_channel(
                        yt_channel_id, _MAX_RECENT_VIDEOS
                    )
                    channels_last_videos[yt_channel_id] = videos

                recent_videos = channels_last_videos[yt_channel_id]
                new_unsent_videos = _get_unsent_videos(
                    recent_videos, rules[yt_channel_id]["last_video_id"]
                )
                for video in new_unsent_videos:
                    await _send_youtube_notification_for_guild(
                        guild_id,
                        rules[yt_channel_id]["discord_channel_id"],
                        video,
                        rules[yt_channel_id].get("custom_text_message"),
                    )
            except:
                _logger.exception(
                    "features/youtube_notify: Failed to process possible "
                    + f"new video notification for channel id '{yt_channel_id}'"
                )


async def check_new_youtube_videos_for_guild(guild_id: int, yt_channel_id: str):
    if not _active:
        return False

    if guild_id == None or yt_channel_id == None:
        return

    subscriptions = data.get_subscriptions()
    if not subscriptions.get(guild_id):
        return

    rules = data.yt_notif_rules_get(guild_id)
    if not rules:
        return

    rule = rules.get(yt_channel_id)
    if not rule:
        return

    try:
        recent_videos = _get_recent_videos_of_youtube_channel(
            yt_channel_id, _MAX_RECENT_VIDEOS
        )
        new_unsent_videos = _get_unsent_videos(
            recent_videos, rule["last_video_id"]
        )
        for video in new_unsent_videos:
            await _send_youtube_notification_for_guild(
                guild_id,
                rule["discord_channel_id"],
                video,
                rule.get("custom_text_message"),
            )
    except:
        _logger.exception(
            "features/youtube_notify: Failed to check for new videos of "
            + f"Youtube channel: {yt_channel_id} in guild ({guild_id})"
        )


def _get_unsent_videos(recent_videos, last_sent_video_id: str):
    unsent_videos = []

    if len(recent_videos) == 0:
        return unsent_videos

    if last_sent_video_id == None:
        unsent_videos.append(recent_videos[0])
        return unsent_videos

    for video in recent_videos:  # Assuming recent_videos are sorted by date (desc)
        if video["id"] == last_sent_video_id:
            break
        unsent_videos.insert(0, video)  # Sort unsent_video by date (asc)

    return unsent_videos


async def _send_youtube_notification_for_guild(
    guild_id: int, channel_id: int, video, custom_message: str = None
):
    discord_channel = client.get_channel(channel_id)
    if not discord_channel:
        _logger.debug(
            "features/youtube_notify: Failed to get channel with id of: "
            + f"{channel_id} in guild: {guild_id}"
        )
        return

    message = f"A new video from **{video['channel_name']}**:point_down_tone1:"
    if custom_message:
        message = custom_message
    message = message.replace("\\n", "\n")
    message = message + f"\nhttps://www.youtube.com/watch?v={video['id']}"
    await discord_channel.send(message)
    _logger.debug(
        f"features/youtube_notify: Sent a youtube video notification. "
        + f"video_id: '{video['id']}' yt_channel: '{video['channel_name']}' "
        + f" channel: '{discord_channel.name}' ({discord_channel.id}) "
        + f" guild: '{discord_channel.guild.name}' ({discord_channel.guild.id}) "
    )
    data.yt_last_video_id_set(
        guild_id,
        video["channel_id"],
        video["channel_name"],
        video["id"],
    )


def get_last_video_of_youtube_channel(yt_channel_id):
    videos = _get_recent_videos_of_youtube_channel(yt_channel_id, max_videos=1)
    if videos is None or len(videos) == 0:
        return None
    return videos[0]


def _get_recent_videos_of_youtube_channel(yt_channel_id: str, max_videos: int):
    _logger.debug(
        "features/youtube_notify: Getting recent Youtube videos "
        + f"with channel id of '{yt_channel_id}'"
    )
    videos = []
    playlist = Playlist(playlist_from_channel_id(yt_channel_id))
    for i in range(min(max_videos, len(playlist.videos))):
        videos.append(
            {
                "id": playlist.videos[i]["id"],
                "channel_name": playlist.videos[i]["channel"]["name"],
                "channel_id": yt_channel_id,
            },
        )
    return videos
