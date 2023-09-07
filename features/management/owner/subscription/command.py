import data
import logging
from .feature import is_active
from commands.helper import handle_command_exception
from bot import client, ADMINS, HOME_GUILDS
from nextcord import Interaction, Permissions, SlashOption

_logger = logging.getLogger("main")


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
            "features/management: Command 'add_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if not is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if interaction.user.id not in ADMINS:
            _logger.debug(
                "features/management: User does not have permission to use command 'add_server' "
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
            _logger.debug(f"features/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_add(str(target_guild), server_id)
        if result == server_id:
            _logger.info(
                f"features/management: Server '{target_guild.name}' ({target_guild.id}) "
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
            "features/management: Command 'edit_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id} active:{active}"
        )
        if not is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if interaction.user.id not in ADMINS:
            _logger.debug(
                "features/management: User does not have permission to use command 'edit_server' "
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
            _logger.debug(f"features/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_edit(server_id, active)
        if result == server_id:
            active_status = "activated" if active else "deactivated"
            _logger.info(
                f"features/management: Server '{target_guild.name}' ({target_guild.id}) "
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
            "features/management: Command 'remove_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if not is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if interaction.user.id not in ADMINS:
            _logger.debug(
                "features/management: User does not have permission to use command 'remove_server' "
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
            _logger.debug(f"features/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_remove(server_id)
        if result == server_id:
            _logger.info(
                f"features/management: Server '{target_guild.name}' ({target_guild.id}) "
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
