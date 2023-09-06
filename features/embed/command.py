import logging
import webcolors
from .feature import is_active
from bot import client
from commands.helper import handle_command_exception
from nextcord import Interaction, SlashOption, Permissions, Embed

_logger = logging.getLogger("main")


@client.slash_command(
    name="embed",
    description=" Send an embed message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def embed(
    interaction: Interaction,
    text: str = SlashOption(
        required=True, description="Enter your text. (Use \\n for new-line)"
    ),
    color: str = SlashOption(
        required=False,
        description="Color name or HEX e.g: red/ff0000, default color is cyan.",
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'embed' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: text:{text} color:{color}"
        )
        if not is_active():
            _logger.info(
                "features/embed: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        default_color = "cyan"
        if color is None:
            color = default_color

        try:
            rgb = webcolors.name_to_rgb(color)
            hex_value = webcolors.rgb_to_hex(rgb)
            embed_color = hex_value.replace("#", "0x")
            embed_color = int(embed_color, base=16)
        except:
            _logger.debug(f"commands/management: Invalid color '{color}'")
            await interaction.send("Invalid color.", ephemeral=True)
            return

        if hex_value is None:
            try:
                embed_color = int(f"0x{color}", base=16)
            except:
                _logger.debug(f"commands/management: Invalid color '{color}'")
                await interaction.send("Invalid color.", ephemeral=True)
                return

        text = text.replace("\\n", "\n")
        embed = Embed(title=text, color=embed_color)
        await interaction.send(embed=embed)
    except:
        await handle_command_exception("embed", interaction)
