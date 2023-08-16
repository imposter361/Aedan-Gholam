import data
import features
import logging
import pytube
import webcolors
from .helper import handle_command_exception
from bot import client, ADMINS, HOME_GUILDS
from nextcord import Interaction, Permissions, SlashOption, Embed
from typing import Optional

_logger = logging.getLogger("main")


# help
@client.slash_command(
    name="help",
    description="Display help message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def help(interaction: Interaction):
    try:
        _logger.info(
            "commands/management: Command 'help' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        help_message = (
            "Salam, AedanGholam dar khedmate shomast.\n\n"
            "`/settings`: Baraye set kardan tanzimate bot az in command estefade konid.\n"
            "`set welcome channel id`: in option baraye set kardane id text channel marboot be payam haye khosh amad gooyi mibashad.\n"
            "`/embed`: baraye neveshtan yek payam dar embed ast ke mitavan az rang haye mokhtalef estefade kard."
        )
        await interaction.send(help_message)
    except:
        await handle_command_exception("help", interaction)


@client.slash_command(
    name="add_server",
    description="Grant permission to a new discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def add_server(interaction: Interaction, id: str = SlashOption(required=True)):
    try:
        _logger.info(
            "commands/management: Command 'add_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'add_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.add_server(str(target_guild), server_id)
        if result == server_id:
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + "has been registered and activated."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been registered and activated.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("add_server", interaction, interaction_response)


@client.slash_command(
    name="edit_server",
    description="Edit permissions of a discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def edit_server(
    interaction: Interaction,
    id: str = SlashOption(required=True),
    active: bool = SlashOption(required=True),
):
    try:
        _logger.info(
            "commands/management: Command 'edit_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id} active:{active}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'edit_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.edit_server(server_id, active)
        if result == server_id:
            active_status = "activated" if active else "deactivated"
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + f"has been {active_status}."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been **{active_status}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("edit_server", interaction, interaction_response)


@client.slash_command(
    name="remove_server",
    description="Remove permission from a discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def remove_server(interaction: Interaction, id: str = SlashOption(required=True)):
    try:
        _logger.info(
            "commands/management: Command 'remove_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'remove_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.remove_server(server_id)
        if result == server_id:
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + "has been removed."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been removed.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception(
            "remove_server", interaction, interaction_response
        )


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
            "Set welcome channel id",
            "Set role message id",
            "Set free game channel id",
            "Set free game role id",
            "Set DST role id",
            "Set member count channel id",
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
                    result = data.set_welcome_channel_id(interaction.guild_id, None)
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

                result = data.set_welcome_channel_id(interaction.guild_id, channel_id)
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

        if setting == "Set free game channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.set_free_games_channel_id(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Free games channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "free game channel has been unset.",
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
                result = data.set_free_games_channel_id(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: Free games channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "free game channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set free game channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set free game role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.set_free_games_role_id(interaction.guild_id, None)
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
                result = data.set_free_games_role_id(interaction.guild_id, role_id)
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
                    result = data.set_dst_role_id(interaction.guild_id, None)
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
                result = data.set_dst_role_id(interaction.guild_id, role_id)
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
                    result = data.set_member_count_channel_id(
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
                result = data.set_member_count_channel_id(
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
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set member count channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set role message id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.set_role_message_id(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Set role message id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit("Role message has been unset."),
                    else:
                        await interaction_response.edit(str(result))
                    return

                message_id = int(id)
                channel = interaction.channel
                message = None
                try:
                    message = await channel.fetch_message(message_id)
                except Exception as e:
                    pass

                if not message:
                    _logger.debug(f"commands/management: Message id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid message id. Make sure to run this command "
                        + "in the same channel as the target message.",
                    )
                    return

                result = data.set_role_message_id(interaction.guild_id, message_id)
                if result == message_id:
                    _logger.info(
                        f"commands/management: Set role message id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Role message has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set role message id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")
    except:
        await handle_command_exception("settings", interaction, interaction_response)


# set roles by emojis
@client.slash_command(
    name="set_role_emoji",
    description="Choose an emoji to assign a roll",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def set_role_emoji(
    interaction: Interaction,
    emoji_name: str = SlashOption(
        name="emoji_name",
        description="CaSe sEnSiTiVe!",
        required=True,
    ),
    role_name: str = SlashOption(
        name="role_name", description="CaSe sEnSiTiVe!", required=True
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'set_role_emoji' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: emoji_name:{emoji_name} "
            + f"role_name:{role_name}"
        )
        interaction_response = await interaction.send(
            f"Please wait ...", ephemeral=True
        )

        get_roles = data.get_role_emoji(interaction.guild_id)
        if get_roles == None:
            get_roles = {}
        if role_name.lower() in ["none", "null", "0", "-"]:
            get_roles.pop(emoji_name)
            _logger.info(
                f"commands/management: Emoji ({emoji_name}) and role ({role_name}) unpaired "
                + f"in '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction_response.edit("Emoji and role unpaired!")
        else:
            get_roles[emoji_name] = role_name
            _logger.info(
                f"commands/management: Emoji ({emoji_name}) and role ({role_name}) paired "
                + f"in '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction_response.edit("Emoji and role paired!")
        data.set_role_emoji(interaction.guild_id, get_roles)
    except:
        await handle_command_exception(
            "set_role_emoji", interaction, interaction_response
        )


# Delete messages
@client.slash_command(
    name="delete",
    description="Delete as many messages as you want",
    default_member_permissions=8,
)
async def delete(
    interaction: Interaction, number: Optional[int] = SlashOption(required=True)
):
    try:
        _logger.info(
            "commands/management: Command 'delete' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)
        if number <= 0:
            await interaction_response.edit(f"{number} is not allowed")
            return

        await interaction.channel.purge(limit=number)

        report = ""
        if number == 1:
            report = f"{number} message has been deleted."
        else:
            report = f"{number} messages have been deleted."

        _logger.info(
            f"commands/management: {report} Guild: '{interaction.guild.name}' ({interaction.guild_id})"
            + f"Channel: '{interaction.channel.name}' ({interaction.channel_id})"
        )
        await interaction_response.edit(f"{report}")

    except:
        await handle_command_exception("delete", interaction, interaction_response)


@client.slash_command(
    name="embed",
    description=" Send an embed message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def embed(
    interaction: Interaction,
    text: str = SlashOption(required=True, description="Write a text in embed"),
    color: str = SlashOption(
        required=False,
        description="Color name or HEX e.g: red/ff0000, default color is cyan.",
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'embed' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: text:{text} color:{color}"
        )
        default_color = "cyan"
        if color is None:
            color = default_color

        try:
            rgb = webcolors.name_to_rgb(color)
            hex_value = webcolors.rgb_to_hex(rgb)
            embed_color = hex_value.replace("#", "0x")
            embed_color = int(embed_color, base=16)
        except:
            _logger.debug(f"commands/management: Invalid color '{color}'")
            await interaction.send("Invalid color.", ephemeral=True)
            return

        if hex_value is None:
            try:
                embed_color = int(f"0x{color}", base=16)
            except:
                _logger.debug(f"commands/management: Invalid color '{color}'")
                await interaction.send("Invalid color.", ephemeral=True)
                return

        embed = Embed(title=text, color=embed_color)
        await interaction.send(embed=embed)
    except:
        await handle_command_exception("embed", interaction)


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

        result = data.add_yt_notif_rule(
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

        result = data.remove_yt_notif_rule(interaction.guild_id, video.channel_id)
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
