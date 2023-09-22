from PIL import Image, ImageDraw, ImageFont

# get an image
with Image.open(r"C:\Users\prash\Downloads\goblin.png").convert("RGBA") as base:

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    
    # get a font
    fnt = ImageFont.truetype(r"C:\USERS\PRASH\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\KOMIKAX.TTF", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10, 10), "Hello", font=fnt, fill=(0, 255, 255, 128))
    # draw text, full opacity
    d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))

    out = Image.alpha_composite(base, txt)

    out.show()