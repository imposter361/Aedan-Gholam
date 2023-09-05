import logging
from bot import client
from commands.helper import handle_command_exception
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
            "commands/management: Command 'help' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        help_message = (
            "Salam\n**AedanGholam** dar khedmate shomast.\n\n"
            "`/settings`: Baraye set kardan tanzimate bot az in command estefade konid.\n"
            "`/set welcome channel id`: in option baraye set kardane id text channel marboot be payam haye khosh amad gooyi mibashad.\n"
            "`/embed`: baraye neveshtan yek payam dar embed ast ke mitavan az rang haye mokhtalef estefade kard."
        )
        await interaction.send(help_message, ephemeral=True)
    except:
        await handle_command_exception("help", interaction)
