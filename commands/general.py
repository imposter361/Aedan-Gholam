import logging
import random
import re
import requests
from .helper import handle_command_exception
from bot import client
from nextcord import Interaction, SlashOption
from version import VERSION

_logger = logging.getLogger("main")


# Hafez
@client.slash_command(name="hafez", description="Fall Migholi ?!")
async def hafez(interaction: Interaction):
    try:
        _logger.info(
            "commands/general: Command 'hafez' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        interaction_response = await interaction.send(f"Please wait ...")
        url = "https://c.ganjoor.net/beyt-xml.php?n=1&a=1&p=2"
        response = requests.get(url)
        xml = response.content
        m1 = xml.split(b"<m1>")[1].split(b"</m1>")[0].decode("utf-8")
        m2 = xml.split(b"<m2>")[1].split(b"</m2>")[0].decode("utf-8")
        poet = xml.split(b"<poet>")[1].split(b"</poet>")[0].decode("utf-8")
        total_poem = xml.split(b"<url>")[1].split(b"</url>")[0].decode("utf-8")
        up = "🖊️"
        poem = f"{m1}\n{m2}\n\n{up} [{poet}]({total_poem})"
        await interaction_response.edit(poem)

    except:
        await handle_command_exception("hafez", interaction, interaction_response)


# Hekmat
@client.slash_command(name="hekmat", description="Yek Hekmat az Nahj al-balagha")
async def hekmat(
    interaction: Interaction,
    number: int = SlashOption(
        required=False, description="Yek adad beyne 1 ta 480 vared konid"
    ),
):
    try:
        _logger.info(
            "commands/general: Command 'hekmat' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        if number is None:
            number = random.randrange(1, 481)
        if number > 480 or number < 1:
            await interaction.response.send_message(
                "Yek adad beyne 1 ta 480 vared konid!", ephemeral=True
            )
            return
        interaction_response = await interaction.send(f"Please wait ...")
        url = f"https://alimaktab.ir/json/wisdom/?n={number}"
        response = requests.get(url)
        response_json = response.json()

        arabic = response_json["main"]
        farsi = response_json["ansarian"]
        hekmat = "حکمت " + str(number) + ": " + arabic + "\n\n" + farsi
        new_string = hekmat.replace("[", "").replace("]", "")

        def remove_html(text):
            clean = re.compile("<.*?>")
            return re.sub(clean, "", text)

        clean_text = remove_html(new_string)
        clean_text = clean_text.replace("&raquo;", "»")
        clean_text = clean_text.replace("&laquo;", "«")

        await interaction_response.edit(clean_text)

    except:
        await handle_command_exception("hekmat", interaction, interaction_response)


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
