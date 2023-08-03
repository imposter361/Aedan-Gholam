import logging
import requests
import random
import re
import data
import pytube
from bot import client
from version import VERSION
from nextcord import Interaction, SlashOption, Permissions
from typing import Optional


# help
@client.slash_command(
    name="help",
    description="Display help message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def help(interaction: Interaction):
    interaction_response = await interaction.send(f"Please wait ...", ephemeral=True)

    help_message = (
        "Salam, AedanGholam dar khedmate shomast.\n\n"
        "`/settings`: Baraye set kardan tanzimate bot az in command estefade konid.\n"
        "`set welcome channel id`: in option baraye set kardane id text channel marboot be payam haye khosh amad gooyi mibashad.\n"
        "`/embed`: baraye neveshtan yek payam dar embed ast ke mitavan az rang haye mokhtalef estefade kard."
    )
    await interaction_response.edit(help_message)


# Hafez
@client.slash_command(name="hafez", description="Fall Migholi ?!")
async def hafez(interaction: Interaction):
    interaction_response = await interaction.send(f"Please wait ...")
    try:
        url = "https://c.ganjoor.net/beyt-xml.php?n=1&a=1&p=2"
        response = requests.get(url)
        xml = response.content
        m1 = xml.split(b"<m1>")[1].split(b"</m1>")[0].decode("utf-8")
        m2 = xml.split(b"<m2>")[1].split(b"</m2>")[0].decode("utf-8")
        poet = xml.split(b"<poet>")[1].split(b"</poet>")[0].decode("utf-8")
        up = "🖊️"
        poem = f"{m1}\n{m2}\n\n{up} {poet}"
        await interaction_response.edit(poem)

    except Exception as e:
        print(str(e) + " Exception happend in Hafez.")
        logging.error(str(e) + " Exception happend in Hafez.")
        await interaction_response.edit(
            f"Bebakhshid moshkeli pish oomade, dobare test kon!"
        )


# Delete messages
@client.slash_command(
    name="delete",
    description="Delete how many messages you want",
    default_member_permissions=8,
)
async def delete(
    interaction: Interaction, number: Optional[int] = SlashOption(required=True)
):
    try:
        interaction_response = await interaction.send("Please wait...", ephemeral=True)
        if number <= 0:
            await interaction_response.edit(f"{number} is not allowed")
            return

        await interaction.channel.purge(limit=number)
        if number == 1:
            await interaction_response.edit(f"{number} message deleted.")
            logging.warning(f"{number} message deleted.")
        else:
            await interaction_response.edit(f"{number} messages have been deleted.")
            logging.warning(f"{number} messages have been deleted.")

    except Exception as e:
        print(str(e) + " Exception happend in Message delete.")
        logging.error(str(e) + " Exception happend in Message delete.")


# About Aedan Team
@client.slash_command(name="team", description="About Aedan Team")
async def team(interaction: Interaction):
    try:
        team = "<:Aedan_logo:1103676392606007356> Bunch of friends gathered together as a team:\n\nEhsan 👨‍💻\nHossein(Moz) 💃\nBagher 🫰\nHossein(Defalcator) 🪡\nAli 🪃\nSina 🧻\n"
        await interaction.response.send_message(team)
    except Exception as e:
        print(str(e) + " Exception happend in Team.")
        logging.error(str(e) + " Exception happend in Team.")


# About Adean Gholam
@client.slash_command(name="about", description="About Gholam")
async def about(interaction: Interaction):
    try:
        Ali = client.get_user(620593942559326265)
        guild_name = client.get_guild(899023632204980324)
        about = f"Gholamam v{VERSION} az **{guild_name}**\nSaakhte daste aghamoon {Ali.mention} kheyli chakerim."
        await interaction.response.send_message(about)
    except Exception as e:
        print(str(e) + " Exception happend in About.")
        logging.error(str(e) + " Exception happend in About.")


# Hekmat
@client.slash_command(name="hekmat", description="Yek Hekmat az Nahj al-balagha")
async def hekmat(
    interaction: Interaction,
    number: int = SlashOption(
        required=False, description="Yek adad beyne 1 ta 480 vared konid"
    ),
):
    if number is None:
        number = random.randrange(1, 481)
    if number > 480 or number < 1:
        await interaction.response.send_message(
            "Yek adad beyne 1 ta 480 vared konid!", ephemeral=True
        )
        return
    interaction_response = await interaction.send(f"Please wait ...")
    try:
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

    except Exception as e:
        print(str(e) + " Exception happend in Hekmat.")
        logging.error(str(e) + " Exception happend in Hekmat.")
        await interaction_response.edit(
            f"Bebakhshid moshkeli pish oomade, dobare test kon!"
        )


@client.slash_command(
    name="youtube",
    description="Send new youtube videos in a channel.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_set(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
    channel_id: str = SlashOption(
        required=True,
        description="Target Discord channel id to publish new youtube videos.",
    ),
):
    try:
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
        video = pytube.YouTube(link)

        result = data.add_yt_notif_rule(
            interaction.guild_id, video.channel_id, channel_id
        )
        if result == video.channel_id or result == "Updated.":
            await interaction_response.edit(
                f"Done. **{video.author}** new videos will be posted on **{channel.name}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except Exception as e:
        print(e)
        await interaction_response.edit(str(e))


@client.slash_command(
    name="youtube_remove",
    description="Remove a previously set notification rule.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_remove(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
):
    try:
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        video = pytube.YouTube(link)

        result = data.remove_yt_notif_rule(interaction.guild_id, video.channel_id)
        if result == video.channel_id:
            await interaction_response.edit(
                f"You will no longer receive new videos from **{video.author}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except Exception as e:
        print(e)
        await interaction_response.edit(str(e))
