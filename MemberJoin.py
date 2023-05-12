import nextcord
from PIL import Image, ImageDraw,ImageFont
from bot import *


# send welcome message for new members:
@client.event
async def on_member_join(member):
    if str(member.guild.id) in SUBSCRIPTIONS and SUBSCRIPTIONS[str(member.guild.id)]:
        guild = member.guild
        channel = client.get_channel(int(WELCOME_CH_ID))
        author_profile_pic = member.avatar
        response = requests.get(author_profile_pic)

        with open("p.png", "wb") as file:
            file.write(response.content)

        # get username and guild member count
        member_name = str(member)
        member_number = f"Now there are ({guild.member_count}) of us"

        # set font
        font = ImageFont.truetype("Bungee-Regular.ttf", 30) # for member name
        font1 = ImageFont.truetype("Bungee-Regular.ttf", 20) # for member counter
        
        # Open the original image
        size = (150, 150) # profile pic size
        img = Image.open("p.png").resize(size)
        size2 = (158, 158) # white circle
        
        # Create a new image with a circular mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        
        circle_bordere = Image.new('RGBA', size2, (255, 255, 255, 0))
        circle_img = Image.new('RGBA', size, (255, 255, 255, 0))
        circle_draw = ImageDraw.Draw(circle_bordere)
        circle_draw.ellipse((0, 0) + size2, fill=(255, 255, 255, 255), outline=(255, 255, 255, 255), width=2)
        circle_img.paste(img, (0, 0), mask=mask)
        
        # Open the background image
        background = Image.open("b.jpg").convert('RGBA')
        
        # Define the position to paste the circular image onto the background image
        position = (280, 83)
        position2 = (276, 79)
        
        # Paste the circular image onto the background image
        background.paste(circle_bordere, position2, circle_bordere)
        background.paste(circle_img, position, circle_img)
        
        # paste booster image top of the profile pic (booster = aedan bird)
        booster = Image.open('s.png').resize((72, 51)).convert('RGBA')
        r, g, b, a = booster.split()
        new_image = Image.new('RGBA', background.size, (255, 255, 255, 0))
        new_image.paste(Image.merge('RGBA', (r, g, b, a)), (320, 212), a)
        background.paste(new_image, (0, 0), new_image)
        
        # write member_number
        text_width, text_height = draw.textsize(member_number, font=font1)
        x2 = (709 - text_width) / 2
        draw2 = ImageDraw.Draw(background)
        draw2.text((x2,25), member_number, fill=(250, 208, 92, 255) , font=font1)

        # write member_name
        draw1 = ImageDraw.Draw(background)
        text_width, text_height = draw.textsize(member_name, font=font)
        x = (709 - text_width) / 2
        draw1.text((x,285), member_name, fill=(250, 208, 92, 255) , font=font)

        # Save the final image
        background.save("final_image.png")    
        file = nextcord.File("final_image.png", filename="welcome.png")   
    
        await channel.send(f"Salam {member.mention} be **{guild}** khosh oomadi!\n", file=file)
        logging.info(f"{member_name} joined {guild}.")

def setup_on_member_join(bot):
    bot.event(on_member_join)