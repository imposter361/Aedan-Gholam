import aiohttp
import data
import logging
import nextcord
from bot import client, HOME_GUILDS
from PIL import Image, ImageDraw, ImageFont

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'welcome_banner'")


# send welcome message for new members:
async def send_welcome_banner(member: nextcord.Member):
    if not _active:
        return False

    try:
        guild = member.guild
        subscriptions = data.get_subscriptions()
        if guild.id not in subscriptions or not subscriptions[guild.id]:
            return

        welcome_channel_id = data.welcome_channel_id_get(guild.id)
        if welcome_channel_id is None:
            return

        _logger.debug(
            f"features/welcome_banner: Generating welcome banner for the new member: "
            + f"'{member.name}' ({member.id}) in '{guild.name}' ({guild.id})"
        )

        channel = client.get_channel(welcome_channel_id)
        if not channel:
            _logger.debug(
                "features/welcome_banner: Failed to get channel with id of: "
                + f"{welcome_channel_id} in guild: {guild.id}"
            )
            return

        is_home = False
        if guild.id in HOME_GUILDS:  # Aedan Gaming server id
            is_home = True
        file = await _create_welcome_banner(member, is_home)
        message: str = f"Salam {member.mention} be **{guild}** khosh oomadi!\n"
        custom_message = data.welcome_message_get(guild.id)

        if custom_message:
            message = custom_message
            message = message.replace("{username}", member.mention)
            message = message.replace("{servername}", guild.name)
        await channel.send(message, file=file)

        _logger.debug(
            f"features/welcome_banner: Welcome banner has been sent for '{member.name}' ({member.id}) "
            + f"at channel '{channel.name}' ({channel.id}) in '{guild.name}' ({guild.id})"
        )
    except:
        _logger.exception(f"features/welcome_banner: Failed to send welcome banner")


async def _create_welcome_banner(member, is_home):
    if member.avatar:
        raw_response = None
        async with aiohttp.ClientSession() as session:
            async with session.get(member.avatar.url) as response:
                if response.status != 200:
                    raise Exception(f"Web request status is {response.status}.")
                raw_response = await response.content.read()

        with open("resources/p.png", "wb") as file:
            file.write(raw_response)
        profile_pic_path = "resources/p.png"
    else:
        profile_pic_path = "resources/NoPic.png"

    # get username and guild member count
    guild = member.guild
    member_name = str(member.name)
    member_number = f"Now there are '{guild.member_count}' of us"

    # set font
    name_font = None
    counter_font = None

    if is_home:
        # for member name
        name_font = ImageFont.truetype("resources/BreeSerif-Regular.ttf", 30)
        # for member counter
        counter_font = ImageFont.truetype("resources/BreeSerif-Regular.ttf", 20)
    else:
        name_font = ImageFont.truetype(
            "resources/Righteous-Regular.ttf", 35
        )  # for member name
        counter_font = ImageFont.truetype(
            "resources/Righteous-Regular.ttf", 25
        )  # for member counter

    # Open the original image
    size = (150, 150)  # profile pic size
    img = Image.open(profile_pic_path).resize(size)
    size2 = (158, 158)  # white circle

    # Create a new image with a circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    circle_bordere = Image.new("RGBA", size2, (255, 255, 255, 0))
    circle_img = Image.new("RGBA", size, (255, 255, 255, 0))
    circle_draw = ImageDraw.Draw(circle_bordere)
    circle_draw.ellipse(
        (0, 0) + size2,
        fill=(255, 255, 255, 255),
        outline=(255, 255, 255, 255),
        width=2,
    )
    circle_img.paste(img, (0, 0), mask=mask)

    # Open the background image
    background = Image.open("resources/b.jpg").convert("RGBA")

    # Define the position to paste the circular image onto the background image
    position = None
    position2 = None
    if is_home:
        position = (280, 83)
        position2 = (276, 79)
    else:
        position = (280, 93)
        position2 = (276, 89)
    # Paste the circular image onto the background image
    background.paste(circle_bordere, position2, circle_bordere)
    background.paste(circle_img, position, circle_img)

    # paste booster image top of the profile pic (booster = aedan bird)
    if is_home:
        booster = Image.open("resources/s.png").resize((72, 51)).convert("RGBA")
        r, g, b, a = booster.split()
        new_image = Image.new("RGBA", background.size, (255, 255, 255, 0))
        new_image.paste(Image.merge("RGBA", (r, g, b, a)), (320, 212), a)
        background.paste(new_image, (0, 0), new_image)

    # write member_number
    text_width, text_height = draw.textsize(member_number, font=counter_font)
    x2 = (709 - text_width) / 2
    draw2 = ImageDraw.Draw(background)
    draw2.text((x2, 25), member_number, fill=(250, 208, 92, 255), font=counter_font)

    # write member_name
    draw1 = ImageDraw.Draw(background)
    text_width, text_height = draw.textsize(member_name, font=name_font)
    x = (709 - text_width) / 2
    draw1.text((x, 285), member_name, fill=(250, 208, 92, 255), font=name_font)

    # Save the final image
    background.save("resources/final_image.png")
    file = nextcord.File("resources/final_image.png", filename="welcome.png")
    return file
