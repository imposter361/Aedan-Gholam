import asyncio
import logging
import random
from .feature import is_active, get_hekmat_text
from bot import client
from commands.helper import handle_command_exception
from nextcord import Interaction, SlashOption

_logger = logging.getLogger("main")


@client.slash_command(name="hekmat", description="Yek Hekmat az Nahj al-balagha")
async def hekmat(
    interaction: Interaction,
    number: int = SlashOption(
        required=False, description="Yek adad beyne 1 ta 480 vared konid"
    ),
):
    try:
        _logger.info(
            "features/hekmat: Command 'hekmat' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        if not is_active():
            _logger.info(
                "features/hekmat: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        if number is None:
            number = random.randrange(1, 481)
        if number > 480 or number < 1:
            await interaction.response.send_message(
                "Yek adad beyne 1 ta 480 vared konid!", ephemeral=True
            )
            return
        task1 = interaction.send(f"Please wait ...")
        task2 = get_hekmat_text(number)
        interaction_response, hekmat_text = await asyncio.gather(task1, task2)
        if not hekmat_text:
            await interaction_response.edit("Something went wrong...")
        else:
            await interaction_response.edit(hekmat_text)
    except:
        await handle_command_exception("hekmat", interaction, interaction_response)
