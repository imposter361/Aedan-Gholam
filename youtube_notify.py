import nextcord
import os
import requests
import pytube
from bot import client
from nextcord.ext import tasks
from nextcord.ext import commands
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from pytube import YouTube, Channel


# Set up Discord bot
# intents = nextcord.Intents.default()
# intents.guilds = True
# intents.messages = True
# bot = commands.Bot(command_prefix="!", intents=intents)


# Set up YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "youtube_client_secrets.json"


# Store the last video ID to check for new videos
last_video_id = None


# @bot.event
# async def on_ready():
#     print("Bot is ready!")


@tasks.loop(seconds=15)
async def check_for_new_youtube_video():
    global last_video_id


    # Authorization flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()

    # Create the YouTube service
    youtube_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Get the latest uploaded video from a specific channel
    request = youtube_service.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="date",
        type="video",
    )

    response = request.execute()

    # Get the video ID of the latest video
    latest_video_id = response["items"][0]["id"]["videoId"]

    # Compare with the last recorded video ID
    if latest_video_id != last_video_id:
        last_video_id = latest_video_id
        # Send a notification message to Discord
        channel = client.get_channel(751641526408314884)
        await channel.send("New YouTube video uploaded!")

    # Check every hour (3600 seconds)
    await nextcord.sleep(3600)


# @bot.command()
# async def start_notify(ctx):
#     # Start checking for new YouTube videos
#     bot.loop.create_task(check_youtube())
#     await ctx.send("YouTube notification started!")


# @bot.command()
# async def stop_notify(ctx):
#     # Stop checking for new YouTube videos
#     bot.loop.stop()
#     await ctx.send("YouTube notification stopped!")


# bot.run("MTA5OTA0MDE0MjE5NjQ5MDI5MA.G_C8G2.HfXFdTuEz0pZbSs7iaMWWdJGAyYAtOtESNjI_o")


# import os
# import nextcord
# from nextcord.ext import commands
# import googleapiclient.discovery

# # Set up Discord client and YouTube API client
# intents = nextcord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)
# youtube_api = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUR_YOUTUBE_API_KEY")

# @bot.event
# async def on_ready():
#     print(f"We have logged in as {bot.user}")

# @bot.command()
# async def notify(ctx, channel_name):
#     # Get the channel ID from YouTube API
#     channel_search = youtube_api.search().list(
#         part="snippet",
#         q=channel_name,
#         type="channel"
#     ).execute()

#     if len(channel_search['items']) == 0:
#         await ctx.send("Channel not found.")
#         return

#     channel_id = channel_search['items'][0]['id']['channelId']

#     # Get the latest video from the channel
#     channel_videos = youtube_api.search().list(
#         part="snippet",
#         channelId=channel_id,
#         type="video",
#         order="date",
#         maxResults=1
#     ).execute()

#     if len(channel_videos['items']) == 0:
#         await ctx.send("No videos found for this channel.")
#         return

#     latest_video_id = channel_videos['items'][0]['id']['videoId']
#     latest_video_url = f"https://www.youtube.com/watch?v={latest_video_id}"

#     # Send notification message to Discord channel
#     await ctx.send(f"New video from {channel_name}: {latest_video_url}")

# # Run the bot
# bot.run("YOUR_DISCORD_BOT_TOKEN")
