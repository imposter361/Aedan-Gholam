import data
import logging
import pytube
from .feature import is_active
from commands.helper import handle_command_exception
from bot import client
from features import youtube_notify
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
):
    try:
        _logger.info(
            "features/management: Command 'youtube' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) "
            + f"args: link:{link} channel_id:{channel_id}"
        )
        if not is_active() or not youtube_notify.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not channel_id:
            channel_id = interaction.channel_id

        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
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
        last_channel_video = youtube_notify.get_last_video_of_youtube_channel(
            video.channel_id
        )

        result = data.yt_notif_rule_add(
            interaction.guild_id,
            video.channel_id,
            video.author,
            channel_id,
            last_channel_video["id"],
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
        if not is_active() or not youtube_notify.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
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
