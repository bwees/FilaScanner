# FilaScanner
I wrote this script to use the webcam already attached to an octoprint instance to scan QR codes on filament spools. It then updates the selected spool in Filament Manager and also shows a success message on printer screen. It also plays a short chime from the printer's buzzer to indicate a successful scan.

Things to Note
- Does not select a spool unless the printer is **on** and **connected to OctoPrint*
- The ID number of the QR code **MUST** be in the spool name in Filament Manager.
  - Example: If the QR Code ID is 11, 11 must be in the name in Filament Manager
    - **VALID**: QR: `11`, Spool Name: `011 - Black PLA` or `Spool 11` or `#11`
    - **INVALID**: QR: `11`, Spool Name: `Black PLA`
- A sheet of labels with IDs 1-30 is included (`label.png`). This is meant to be printed on Avery 5160 Address Labels and applied to each spool. 
  - If you wish to make more labels, use the `label_maker.py` program. Change the `startID` to whatever ID you want. It will generate a new `label.png` image that you can then print.
- If you do not want to use the included label maker, the format for the QR code text payload is `SPOOL - # - SPOOL`. 
  - Replace the `#` with whatever spool ID you have in the name in Filament Manager.
  - A number MUST be between the dashes in the payload of the QR code

❗ This project has been only tested with Python 3. As such, the service targets Python 3 as the executon environment. If you still are using Python 2 in Octoprint, please see here: https://octoprint.org/blog/2020/09/10/upgrade-to-py3/

## Install Steps
1. `$ cd && git clone https://github.com/bwees/FilaScanner && cd FilaScanner`
2. Open `filascanner.py` and set `API_KEY` to the OctoPrint API Key 
2. `$ sudo apt install libzbar0`
3. `$ sudo pip3 install pyzbar pillow pyqrcode`
4. `$ sudo cp filascanner.service /etc/systemd/system/filascanner.service`
5. `$ sudo systemctl daemon-reload && sudo systemctl enable filascanner.service && sudo systemctl start filascanner.service`
6. Place a valid QR code label in front of the octoprint webcam with your printer connected. Printer will beep and show a message on the display.
