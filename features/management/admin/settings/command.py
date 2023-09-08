import data
import features
import logging
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
        description="Available variables: {username} and {servername}, **Bold**",
    ),
):
    print(message)
    # try:
    _logger.info(
        "features/management: Command 'customize' was called by "
        + f"'{interaction.user.name}' ({interaction.user.id}) "
        + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: customize:{customize} message:{message}"
    )
    if not is_active():
        _logger.info(
            "features/management: This feature is not active. Command dismissed."
        )
        await interaction.send(
            f"Sorry! This feature is unavailable at the moment...", ephemeral=True
        )
        return

    interaction_response = await interaction.send("Please wait...", ephemeral=True)
    if customize == "welcome message":
        try:
            if message != None:
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
                    await interaction_response.edit("Welcome message has been set.")
                return

            channel_id = int(id)
            channel = client.get_channel(channel_id)
            if interaction.guild_id != channel.guild.id:
                _logger.debug(f"features/management: Channel id ({id}) is invalid.")
                await interaction_response.edit(
                    "Invalid channel ID.",
                )
                return

            result = data.welcome_message_set(interaction.guild_id, channel_id)
            if result == channel_id:
                _logger.info(
                    f"features/management: Welcome message has been set to {id} "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Welcome channel has been set.",
                )
            else:
                await interaction_response.edit(str(result))
        except:
            _logger.exception(
                f"features/management: Failed to set welcome message ({id}) "
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
            "features/management: Command 'settings' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: setting:{setting} id:{id}"
        )
        if not is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)
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
