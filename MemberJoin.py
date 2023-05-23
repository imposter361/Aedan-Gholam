import logging
import nextcord
import requests
from data import get_welcome_channel_id
from bot import client, SUBSCRIPTIONS, HOME_GUILDS
from PIL import Image, ImageDraw, ImageFont


def create_welcome_banner(member, is_home):
    author_profile_pic = member.avatar
    response = requests.get(author_profile_pic)

    with open("p.png", "wb") as file:
        file.write(response.content)

    # get username and guild member count
    guild = member.guild
    member_name = str(member)
    member_number = f"Now there are '{guild.member_count}' of us"

    # set font
    name_font = None
    counter_font = None

    if is_home:
        # for member name
        name_font = ImageFont.truetype(
            "BreeSerif-Regular.ttf", 30
        )
        # for member counter
        counter_font = ImageFont.truetype(
            "BreeSerif-Regular.ttf", 20
        )
    else:
        name_font = ImageFont.truetype(
            "Righteous-Regular.ttf", 35
        )  # for member name
        counter_font = ImageFont.truetype(
            "Righteous-Regular.ttf", 25
        )  # for member counter

    # Open the original image
    size = (150, 150)  # profile pic size
    img = Image.open("p.png").resize(size)
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
    background = Image.open("b.jpg").convert("RGBA")

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
        booster = Image.open("s.png").resize((72, 51)).convert("RGBA")
        r, g, b, a = booster.split()
        new_image = Image.new("RGBA", background.size, (255, 255, 255, 0))
        new_image.paste(Image.merge("RGBA", (r, g, b, a)), (320, 212), a)
        background.paste(new_image, (0, 0), new_image)

    # write member_number
    text_width, text_height = draw.textsize(member_number, font=counter_font)
    x2 = (709 - text_width) / 2
    draw2 = ImageDraw.Draw(background)
    draw2.text((x2, 25), member_number, fill=(
        250, 208, 92, 255), font=counter_font)

    # write member_name
    draw1 = ImageDraw.Draw(background)
    text_width, text_height = draw.textsize(member_name, font=name_font)
    x = (709 - text_width) / 2
    draw1.text((x, 285), member_name, fill=(250, 208, 92, 255), font=name_font)

    # Save the final image
    background.save("final_image.png")
    file = nextcord.File("final_image.png", filename="welcome.png")
    return file


# send welcome message for new members:
@client.event
async def on_member_join(member):
    guild = member.guild
    if not (guild.id in SUBSCRIPTIONS and SUBSCRIPTIONS[guild.id]):
        return

    welcome_channel_id = get_welcome_channel_id(guild.id)
    if welcome_channel_id is None:
        return

    channel = client.get_channel(welcome_channel_id)
    member_name = str(member)
    is_home = False
    if guild.id == HOME_GUILDS:  # Aedan Gaming server id
        is_home = True
    file = create_welcome_banner(member, is_home)
    await channel.send(
        f"Salam {member.mention} be **{guild}** khosh oomadi!\n", file=file
    )
    print(f"{member_name} joined {guild}.")
    logging.info(f"{member_name} joined {guild}.")
