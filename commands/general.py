import logging
from .helper import handle_command_exception
from bot import client
from nextcord import Interaction
from version import VERSION

_logger = logging.getLogger("main")


# About Aedan Team
@client.slash_command(name="team", description="About Aedan Team")
async def team(interaction: Interaction):
    try:
        _logger.info(
            "commands/general: Command 'team' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        team = (
            "<:Aedan_logo:1103676392606007356> Bunch of friends gathered together "
            + "as a team:\n\nEhsan 👨‍💻\nHossein(Moz) 💃\nBagher 🫰\nHossein(Defalcator) 🪡\nAli 🪃\nSina 🧻"
        )
        await interaction.response.send_message(team)
    except:
        await handle_command_exception("team", interaction)


# About Adean Gholam
@client.slash_command(name="about", description="About Gholam")
async def about(interaction: Interaction):
    try:
        _logger.info(
            "commands/general: Command 'about' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        Ali = client.get_user(620593942559326265)
        guild_name = client.get_guild(899023632204980324)
        about = (
            f"Gholamam v{VERSION} az [**{guild_name}**](https://discord.gg/ZJVhgBCw3Q)\n"
            + f"Saakhte daste aghamoon {Ali.mention}\n"
            + f"kheyli chakerim.<:blobheart:995573025795747900>\n"
            + f"Also add my twin brother [**Radio gholam**](https://discord.com/api/oauth2/authorize?client_id=1107647185111224420&permissions=0&scope=bot) to your server!"
        )
        await interaction.response.send_message(about)
    except:
        await handle_command_exception("about", interaction)
