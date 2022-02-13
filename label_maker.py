from PIL import Image, ImageDraw, ImageFont
import pyqrcode

start_pos = (20, 25)
spacing = (290, 105)

page = Image.new('RGBA', (850, 1100), (255, 255, 255, 255))
xloc = start_pos[0]
yloc = start_pos[1]

font = ImageFont.truetype(r'roboto.ttf', 24)

startID = 1
labelsPerPage = 30

# Import QRCode from pyqrcode

# String which represents the QR code
h = "SPOOL - "
f = " - SPOOL"

for i in range(startID,startID+labelsPerPage):
    # Generate QR code
    url = pyqrcode.create(h + str(i) + f)

    # Create and save the png file naming "myqr.png"
    url.png("out/" + str(i) + '.png', scale = 3)

# for each img in out folder
for i in range(startID,startID+labelsPerPage):
    img = Image.open('out/' + str(i) + '.png')
    page.paste(img, (xloc, yloc))

    # write id number from i next to each img pasted
    draw = ImageDraw.Draw(page)
    draw.text((xloc + 110, yloc + 30), "Spool #" + str(i), (0, 0, 0), font=font)

    xloc += spacing[0]
    if xloc > 700:
        xloc = start_pos[0]
        yloc += spacing[1]


page.save('label.png')