from PIL import Image, ImageDraw

# Open the original image
img = Image.open("p.jpg")

# Define the desired size of the circular image
size = (200, 200)
size2 = (210, 210)


# Resize the original image to the desired size
img = img.resize(size)

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
background = Image.open("b.jpg")

# Define the position to paste the circular image onto the background image
position = (100, 100)
position2 = (95, 95)

# Paste the circular image onto the background image
background.paste(circle_bordere, position2, circle_bordere)
background.paste(circle_img, position, circle_img)

# Save the final image
background.save("final_image.jpg")
