import asyncio
import logging
from .feature import is_active, get_hafez_poem_text
from bot import client
from features._shared.helper import handle_command_exception
from nextcord import Interaction

_logger = logging.getLogger("main")


@client.slash_command(name="hafez", description="Fall Migholi ?!")
async def hafez(interaction: Interaction):
    try:
        _logger.info(
            "features/hafez: Command 'hafez' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        if not is_active():
            _logger.info(
                "features/hafez: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        task1 = interaction.send("Please wait...")
        task2 = get_hafez_poem_text()
        interaction_response, poem = await asyncio.gather(task1, task2)
        if not poem:
            await interaction_response.edit("Something went wrong...")
        else:
            await interaction_response.edit(poem)
    except:
        await handle_command_exception("hafez", interaction, interaction_response)
