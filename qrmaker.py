
# Import QRCode from pyqrcode
import pyqrcode
import png
from pyqrcode import QRCode

# String which represents the QR code
h = "SPOOL - "
f = " - SPOOL"

for i in range(1,31):
    # Generate QR code
    url = pyqrcode.create(h + str(i) + f)

    # Create and save the png file naming "myqr.png"
    url.png("out/" + str(i) + '.png', scale = 3)