import logging
from nextcord import Interaction, PartialInteractionMessage

_logger = logging.getLogger("main")


async def handle_command_exception(
    command_name: str,
    interaction: Interaction,
    interaction_response: PartialInteractionMessage = None,
):
    _logger.exception(f"Exception occurred in the '{command_name}' command.")
    try:
        if interaction_response:
            await interaction_response.edit(content=f"Operation failed.")
        else:
            await interaction.send(content=f"Operation failed.")
    except:
        _logger.exception(
            "Exception occurred when sending an error message to the user."
        )
