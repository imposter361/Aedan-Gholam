import logging
from .feature import is_active
from bot import client
from commands.helper import handle_command_exception
from nextcord import Interaction, SlashOption
from typing import Optional

_logger = logging.getLogger("main")


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
            "features/delete: Command 'delete' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        if not is_active():
            _logger.info(
                "features/delete: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

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
            f"features/delete: {report} Guild: '{interaction.guild.name}' ({interaction.guild_id})"
            + f"Channel: '{interaction.channel.name}' ({interaction.channel_id})"
        )
        await interaction_response.edit(f"{report}")

    except:
        await handle_command_exception("delete", interaction, interaction_response)
