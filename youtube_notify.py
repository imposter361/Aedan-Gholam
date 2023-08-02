import data
from bot import client
from nextcord.ext import tasks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import InstalledAppFlow


# Set up YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "youtube_client_secrets.json"


@tasks.loop(minutes=10)
async def check_for_new_youtube_video():
    subscriptions = data.get_subscriptions()

    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        rules = data.get_yt_notif_rules(guild_id)
        for yt_channel_id in rules:
            try:
                last_video_id = get_last_video_id_of_youtube_channel(yt_channel_id)
                if rules[yt_channel_id]["last_video_id"] != last_video_id:
                    # send message
                    discord_channel = client.get_channel(
                        rules[yt_channel_id]["discord_channel_id"]
                    )
                    discord_channel.send(
                        f"https://www.youtube.com/watch?v={last_video_id}"
                    )
                    # update stored last video id
                    data.set_yt_last_video_id(guild_id, yt_channel_id, last_video_id)
            except Exception as e:
                print(e)


def get_last_video_id_of_youtube_channel(yt_channel_id):
    # Authorization flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()

    # Create the YouTube service
    youtube_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Get the latest uploaded video from a specific channel
    request = youtube_service.search().list(
        part="snippet",
        channelId=yt_channel_id,
        maxResults=1,
        order="date",
        type="video",
    )

    response = request.execute()

    # Get the video ID of the latest video
    latest_video_id = response["items"][0]["id"]["videoId"]

    return latest_video_id
