import data
import features
import logging
import pytube
from .helper import handle_command_exception
from bot import client
from nextcord import Interaction, Permissions, SlashOption

_logger = logging.getLogger("main")


@client.slash_command(
    name="customize",
    description="customize bot settings.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def customize(
    interaction: Interaction,
    customize: str = SlashOption(
        name="customize",
        required=True,
        choices=[
            "welcome message",
        ],
    ),
    message: str = SlashOption(
        required=True,
        description="Available variables: {username} and {servername}, **Bold**",
    ),
):
    print(message)
    # try:
    _logger.info(
        "commands/management: Command 'customize' was called by "
        + f"'{interaction.user.name}' ({interaction.user.id}) "
        + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: customize:{customize} message:{message}"
    )
    interaction_response = await interaction.send("Please wait...", ephemeral=True)
    if customize == "welcome message":
        try:
            if message != None:
                result = data.welcome_message_set(interaction.guild_id, message)
                if result == None:
                    _logger.info(
                        "commands/management: Welcome message has been unset "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Welcome message has been unset.",
                    )
                else:
                    await interaction_response.edit("Welcome message has been set.")
                return

            channel_id = int(id)
            channel = client.get_channel(channel_id)
            if interaction.guild_id != channel.guild.id:
                _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                await interaction_response.edit(
                    "Invalid channel ID.",
                )
                return

            result = data.welcome_message_set(interaction.guild_id, channel_id)
            if result == channel_id:
                _logger.info(
                    f"commands/management: Welcome message has been set to {id} "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Welcome channel has been set.",
                )
            else:
                await interaction_response.edit(str(result))
        except:
            _logger.exception(
                f"commands/management: Failed to set welcome message ({id}) "
                + f"in guild ({interaction.guild_id})"
            )
            await interaction_response.edit("Operation failed.")


@client.slash_command(
    name="settings",
    description="Change bot settings.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def settings(
    interaction: Interaction,
    setting: str = SlashOption(
        name="setting",
        required=True,
        choices=[
            "Set DST role id",
            "Set epic games channel id",
            "Set free game role id",
            "Set klei links channel id",
            "Set member count channel id",
            "Set welcome channel id",
        ],
    ),
    id: str = SlashOption(required=True),
):
    try:
        _logger.info(
            "commands/management: Command 'settings' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: setting:{setting} id:{id}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)
        if setting == "Set welcome channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.welcome_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Welcome channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "Welcome channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return

                result = data.welcome_channel_id_set(interaction.guild_id, channel_id)
                if result == channel_id:
                    _logger.info(
                        f"commands/management: Welcome channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Welcome channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set welcome channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set epic games channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.epic_games_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: epic games channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "epic games channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.epic_games_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: epic games channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "epic games channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set epic games channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set klei links channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.klei_links_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: klei links channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "klei links channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.klei_links_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: klei links channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "klei links channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set klei links channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set free game role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.free_games_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Free game role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "Free game role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                result = data.free_games_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"commands/management: Free game role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Free game role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set free game role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set DST role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.dst_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: DST role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "DST role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                result = data.dst_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"commands/management: DST role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "DST role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set DST role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set member count channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.member_count_channel_id_set(
                        interaction.guild_id, None
                    )
                    if result == None:
                        _logger.info(
                            "commands/management: Member count channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "member count channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.member_count_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: Member count channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "member count channel has been set.",
                    )
                    # Update member count for the first time
                    await features.member_count.update_member_count_for_guild(
                        interaction.guild_id
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set member count channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")
    except:
        await handle_command_exception("settings", interaction, interaction_response)


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
            "commands/management: Command 'youtube' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) "
            + f"args: link:{link} channel_id:{channel_id}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not features.youtube_notify.is_active():
            await interaction_response.edit(
                "Sorry! This feature is unavailable at the moment...",
            )
            return

        if not channel_id:
            channel_id = interaction.channel_id

        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
        if interaction.guild_id != channel.guild.id:
            _logger.debug(
                "commands/management: Invalid discord channel "
                + "or the specified channel belongs to another guild "
                + f"channel_id: {channel_id}"
            )
            await interaction_response.edit(
                "Invalid channel ID.",
            )
            return

        video = pytube.YouTube(link)
        last_channel_video = features.youtube_notify.get_last_video_of_youtube_channel(
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
                f"commands/management: {video.author}'s new youtube videos "
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
            "commands/management: Command 'youtube_remove' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: link:{link}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not features.youtube_notify.is_active():
            await interaction_response.edit(
                "Sorry! This feature is unavailable at the moment...",
            )
            return

        video = pytube.YouTube(link)

        result = data.yt_notif_rule_remove(interaction.guild_id, video.channel_id)
        if result == video.channel_id:
            _logger.info(
                f"commands/management: {video.author}'s new youtube videos will no longer "
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
