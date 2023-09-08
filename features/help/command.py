import logging
from .feature import is_active
from bot import client
from features._shared.helper import handle_command_exception
from nextcord import Interaction, Permissions

_logger = logging.getLogger("main")


@client.slash_command(
    name="help",
    description="Display help message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def help(interaction: Interaction):
    try:
        _logger.info(
            "features/help: Command 'help' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        if not is_active():
            _logger.info(
                "features/help: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        help_message = (
            "Salam\n**AedanGholam** dar khedmate shomast.\n\n"
            "`/settings`: Baraye set kardan tanzimate bot az in command estefade konid.\n"
            "`/set welcome channel id`: in option baraye set kardane id text channel marboot be payam haye khosh amad gooyi mibashad.\n"
            "`/embed`: baraye neveshtan yek payam dar embed ast ke mitavan az rang haye mokhtalef estefade kard."
        )
        await interaction.send(help_message, ephemeral=True)
    except:
        await handle_command_exception("help", interaction)
