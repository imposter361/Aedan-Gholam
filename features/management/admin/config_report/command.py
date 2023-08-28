import data
import io
import logging
from . import feature
from bot import client
from commands.helper import handle_command_exception
from nextcord import Interaction, Permissions, File

_logger = logging.getLogger("main")


@client.slash_command(
    name="get_config",
    description="See your server configs",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def configs_get(
    interaction: Interaction,
):
    try:
        _logger.info(
            "commands/management: Command 'get_config' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        result = data.configs_get(interaction.guild_id)
        refined_config_text = feature.generate_refined_config_text(result, interaction.guild_id)
        file = File(
            io.BytesIO(bytes(refined_config_text, "utf-8")),
            f"{interaction.guild.name}_configs.txt",
        )
        await interaction_response.edit(
            content="Here is your server configs!", files=[file]
        )

    except:
        await handle_command_exception("config", interaction, interaction_response)
