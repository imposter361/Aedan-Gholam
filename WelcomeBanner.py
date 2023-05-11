from PIL import Image, ImageDraw, ImageFilter,ImageFont
from bot import *

member = "Imposter#3060"
font = ImageFont.truetype("Bungee-Regular.ttf", 25)


# Open the original image
size = (150, 150)
img = Image.open("p.jpg").resize(size)
size2 = (158, 158)

# Create a new image with a circular mask
mask = Image.new('L', size, 0)
# mask = mask.filter(ImageFilter.GaussianBlur(radius=5))
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + size, fill=255)

mask1 = Image.new('RGBA', (400,400), 0)
draw =ImageDraw.Draw(mask)
text_width, text_height = draw.textsize(member, font)
draw.text((50,50), member, fill=100 , font=font)

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

booster = Image.open('s.png').resize((145, 103)).convert('RGBA')
r, g, b, a = booster.split()
new_image = Image.new('RGBA', background.size, (255, 255, 255, 0))
new_image.paste(Image.merge('RGBA', (r, g, b, a)), (55, 155), a)
background.paste(new_image, (0, 0), new_image)
background.save("image.png")

# Save the final image
background.save("final_image.png")

