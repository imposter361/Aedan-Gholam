from PIL import Image, ImageDraw,ImageFont
from bot import *


member_name = "Dr.Imposter#3060"
member_number = "Now there are 27 of us"

font = ImageFont.truetype("Bungee-Regular.ttf", 30) # for member name
font1 = ImageFont.truetype("Bungee-Regular.ttf", 20) # for member counter

# Open the original image
size = (150, 150) # profile pic size
img = Image.open("p.jpg").resize(size)
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
position = (52, 53)
position2 = (48, 49)

# Paste the circular image onto the background image
background.paste(circle_bordere, position2, circle_bordere)
background.paste(circle_img, position, circle_img)

# paste booster image top of the profile pic (booster = aedan bird)
booster = Image.open('s.png').resize((145, 103)).convert('RGBA')
r, g, b, a = booster.split()
new_image = Image.new('RGBA', background.size, (255, 255, 255, 0))
new_image.paste(Image.merge('RGBA', (r, g, b, a)), (55, 155), a)
background.paste(new_image, (0, 0), new_image)

# write member_name
draw1 = ImageDraw.Draw(background)
draw1.text((230,130), member_name, fill=(255, 255, 255, 255) , font=font)

# write member_number
draw2 = ImageDraw.Draw(background)
draw2.text((230,180), member_number, fill=(255, 255, 255, 255) , font=font1)


# Save the final image
background.save("final_image.png")