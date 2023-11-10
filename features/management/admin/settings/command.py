import data
import features
import logging
import nextcord
from .feature import is_active
from features._shared.helper import handle_command_exception
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
        description="Available variables: {username} and {servername}. Markdown supported. \\n for new-line",
    ),
):
    _logger.info(
        "features/management: Command 'customize' was called by "
        + f"'{interaction.user.name}' ({interaction.user.id}) "
        + f"in '{interaction.guild.name}' ({interaction.guild_id}) "
        + f"args: customize: '{customize}' message: '{message}'"
    )
    if not is_active():
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
    if customize == "welcome message":
        try:
            message = message.replace("\\n", "\n")
            result = data.welcome_message_set(interaction.guild_id, message)
            if result == None:
                _logger.info(
                    "features/management: Welcome message has been unset "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Welcome message has been unset.",
                )
            else:
                _logger.info(
                    "features/management: Welcome message has been set "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit("Welcome message has been set.")
            return
        except:
            _logger.exception(
                f"features/management: Failed to set welcome message "
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
            "Set CS2 announcements channel id",
            "Set CS2 role id",
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
            "features/management: Command 'settings' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: setting:{setting} id:{id}"
        )
        if not is_active():
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
        if setting == "Set CS2 announcements channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.cs2_announcements_channel_id_set(
                        interaction.guild_id, None
                    )
                    if result == None:
                        _logger.info(
                            "features/management: CS2 announcements channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "CS2 announcements channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
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
                    _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.cs2_announcements_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"features/management: CS2 announcements channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "CS2 announcements channel has been set.",
                    )
                    # Update CS2 announcements for the first time
                    await features.cs2_announcements.check_cs2_announcements_for_guild(
                        interaction.guild_id
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set CS2 announcements channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set CS2 role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.cs2_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: CS2 role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "CS2 role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                role = nextcord.utils.get(interaction.guild.roles, id=role_id)
                if not role:
                    _logger.debug(
                        "features/management: Failed to get role with id of: "
                        + f"{role_id} in guild: {interaction.guild_id}"
                    )
                    await interaction_response.edit(
                        "Invalid role ID.",
                    )
                    return

                result = data.cs2_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"features/management: CS2 role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "CS2 role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set CS2 role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set welcome channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.welcome_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: Welcome channel id has been unset "
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
                    _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return

                result = data.welcome_channel_id_set(interaction.guild_id, channel_id)
                if result == channel_id:
                    _logger.info(
                        f"features/management: Welcome channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Welcome channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set welcome channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set epic games channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.epic_games_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: epic games channel id has been unset "
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
                    _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.epic_games_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"features/management: epic games channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "epic games channel has been set.",
                    )
                    # Check epic games for this guild for the first time
                    await features.epic_games.check_free_games_for_guild(
                        interaction.guild_id
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set epic games channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set klei links channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.klei_links_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: klei links channel id has been unset "
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
                    _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.klei_links_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"features/management: klei links channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "klei links channel has been set.",
                    )
                    # Check klei links for this guild for the first time
                    await features.klei_points.check_klei_points_for_guild(
                        interaction.guild_id
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set klei links channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set free game role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.free_games_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: Free game role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "Free game role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                role = nextcord.utils.get(interaction.guild.roles, id=role_id)
                if not role:
                    _logger.debug(
                        "features/management: Failed to get role with id of: "
                        + f"{role_id} in guild: {interaction.guild_id}"
                    )
                    await interaction_response.edit(
                        "Invalid role ID.",
                    )
                    return

                result = data.free_games_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"features/management: Free game role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Free game role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set free game role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set DST role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.dst_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "features/management: DST role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "DST role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                role = nextcord.utils.get(interaction.guild.roles, id=role_id)
                if not role:
                    _logger.debug(
                        "features/management: Failed to get role with id of: "
                        + f"{role_id} in guild: {interaction.guild_id}"
                    )
                    await interaction_response.edit(
                        "Invalid role ID.",
                    )
                    return

                result = data.dst_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"features/management: DST role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "DST role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"features/management: Failed to set DST role id ({id}) "
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
                            "features/management: Member count channel id has been unset "
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
                    _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.member_count_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"features/management: Member count channel id has been set to {id} "
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
                    f"features/management: Failed to set member count channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")
    except:
        await handle_command_exception("settings", interaction, interaction_response)
