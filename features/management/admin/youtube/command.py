import data
import features
import logging
import pytube
from .feature import is_active
from features._shared.helper import handle_command_exception
from bot import client
from nextcord import Interaction, Permissions, SlashOption

_logger = logging.getLogger("main")


@client.slash_command(
    name="youtube",
    description="Send new youtube videos in a channel.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_set(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
    channel_id: str = SlashOption(
        required=False,
        description="Target Discord channel id to publish new youtube videos.",
    ),
    custom_message: str = SlashOption(
        required=False,
        description="Use '\\n' for new line. Leave empty to use the default message.",
    ),
    send_latest_video: bool = SlashOption(
        required=False,
        default=False,
        description="Choose true if you want to get the current latest video from this Youtube channel.",
    ),
):
    try:
        _logger.info(
            "features/management: Command 'youtube' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) "
            + f"args: link:{link} channel_id:{channel_id}"
        )
        if not is_active() or not features.youtube_notify.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                "Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if not data.get_subscriptions().get(interaction.guild_id):
            _logger.debug(
                f"features/management: Guild ({interaction.guild_id}) "
                + "is not active. Command dismissed."
            )
            await interaction.send(
                "The server's subscription is not active. Please contact bot admin.",
                ephemeral=True,
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not channel_id:
            channel_id = interaction.channel_id

        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
        if not channel:
            _logger.debug(
                "features/management: Failed to get channel with id of: "
                + f"{channel_id} in guild: {interaction.guild_id}"
            )
            await interaction_response.edit(
                "Could not access this Discord channel.",
            )
            return

        if interaction.guild_id != channel.guild.id:
            _logger.debug(
                "features/management: Invalid discord channel "
                + "or the specified channel belongs to another guild "
                + f"channel_id: {channel_id}"
            )
            await interaction_response.edit(
                "Invalid channel ID.",
            )
            return

        video = pytube.YouTube(link)
        last_channel_video_id = None
        if not send_latest_video:
            # If user wants to get the current latest video,
            # leave last_channel_video_id = null so the latest video
            # will be processed in the near future
            last_channel_video = (
                features.youtube_notify.get_last_video_of_youtube_channel(
                    video.channel_id
                )
            )
            last_channel_video_id = last_channel_video["id"]

        result = data.yt_notif_rule_add(
            interaction.guild_id,
            video.channel_id,
            video.author,
            channel_id,
            last_channel_video_id,
            custom_message,
        )
        if result == video.channel_id or result == "Updated.":
            _logger.info(
                f"features/management: {video.author}'s new youtube videos "
                + f"will be posted on '{channel.name}' ({channel.id})"
            )
            await interaction_response.edit(
                f"Done. **{video.author}** new videos will be posted on **{channel.name}**.",
            )
            if send_latest_video:
                # Check videos of this Youtube channel for the first time
                await features.youtube_notify.check_new_youtube_videos_for_guild(
                    interaction.guild_id, video.channel_id
                )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("youtube", interaction, interaction_response)


@client.slash_command(
    name="youtube_remove",
    description="Remove a previously set notification rule.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_remove(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
):
    try:
        _logger.info(
            "features/management: Command 'youtube_remove' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: link:{link}"
        )
        if not is_active() or not features.youtube_notify.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                "Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        video = pytube.YouTube(link)

        result = data.yt_notif_rule_remove(interaction.guild_id, video.channel_id)
        if result == video.channel_id:
            _logger.info(
                f"features/management: {video.author}'s new youtube videos will no longer "
                + f"be posted on '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction_response.edit(
                f"You will no longer receive new videos from **{video.author}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception(
            "youtube_remove", interaction, interaction_response
        )
