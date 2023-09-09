import aiohttp
import logging
from nextcord import Interaction, PartialInteractionMessage

_logger = logging.getLogger("main")


async def handle_command_exception(
    command_name: str,
    interaction: Interaction,
    interaction_response: PartialInteractionMessage = None,
):
    _logger.exception(f"commands: Exception occurred in the '{command_name}' command.")
    try:
        if interaction_response:
            await interaction_response.edit(content=f"Operation failed.")
        else:
            await interaction.send(content=f"Operation failed.")
    except:
        _logger.exception(
            "commands/helper: Exception occurred while sending an error message to the user."
        )


async def aiohttp_get(url: str):
    raw_response = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Get response status was {response.status}")
            raw_response = await response.content.read()

    return raw_response
