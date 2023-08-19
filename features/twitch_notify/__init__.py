import data
import logging
import requests
from bot import client, TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN


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


async def check_for_twitch_live():
    if not _active:
        return False

    _logger.debug("features/youtube_notify: Running Youtube notify task...")

    channels_last_videos = {}

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        rules = data.get_yt_notif_rules(guild_id)
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
                    data.set_yt_last_video_id(
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


async def check_twitch_stream(user_id):
    TWITCH_API_ENDPOINT = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}",
    }

    params = {"user_id": user_id}
    response = requests.get(TWITCH_API_ENDPOINT, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        # Check if there is at least one stream in the data returned by the API
        if len(data["data"]) > 0:
            print(f"{TWITCH_CHANNEL_NAME} is live on Twitch!")

            # Get the first stream from the data returned by the API
            stream_data = data["data"][0]

            # Get the stream title and URL
            stream_title = stream_data["title"]
            stream_url = f"https://www.twitch.tv/{TWITCH_CHANNEL_NAME}"

            # Create an embed message with the stream information
            embed = nextcord.Embed(
                title="Twitch Stream Notification",
                description=f"{TWITCH_CHANNEL_NAME} is live on Twitch!",
                color=nextcord.Color.purple(),
            )
            embed.add_field(name="Title", value=stream_title, inline=False)
            embed.add_field(
                name="Watch Now", value=f"[{stream_url}]({stream_url})", inline=False
            )

            # Get the Discord channel to send the notification to
            await nextcord.message(channel)
            # Send the embed message to the Discord channel
            # await channel.send(embed=embed)
        else:
            print(f"{TWITCH_CHANNEL_NAME} is'n live on Twitch!")
