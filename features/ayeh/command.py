import asyncio
import logging
import random
from .feature import is_active, get_ayeh_text
from bot import client
from features._shared.helper import handle_command_exception
from nextcord import Interaction, SlashOption

_logger = logging.getLogger("main")


@client.slash_command(name="ayeh", description="Yek ayeh az Quran.")
async def ayeh(
    interaction: Interaction,
    number=SlashOption(
        required=False, description="Shomarey ayeh: e.g: 6236 or 114:6 "
    ),
):

    try:
        _logger.info(
            "features/ayeh: Command 'ayeh' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        if not is_active():
            _logger.info(
                "features/ayeh: This feature is not active. Command dismissed."
            )
            await interaction.send(
                "Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if number is None:
            number = random.randrange(1, 6236)

        task1 = interaction.send("Please wait...")
        task2 = get_ayeh_text(number)
        interaction_response, ayeh_text = await asyncio.gather(task1, task2)
        if not ayeh_text:
            await interaction_response.edit("Something went wrong...")
        elif ayeh_text== "404":
            await interaction_response.edit("Invalid ayeh number...")
        else:
            await interaction_response.edit(ayeh_text)
    except:
        await handle_command_exception("ayeh", interaction, interaction_response)
