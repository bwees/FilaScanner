# FilaScanner
I wrote this script to use the webcam already attached to an octoprint instance to scan QR codes on filament spools. It then updates the selected spool in Filament Manager and also shows a success message on printer screen. It also plays a short chime from the printer's buzzer to indicate a successful scan.

Things to Note
- Does not select a spool unless the printer is **on** and **connected to OctoPrint*
- The ID number of the QR code **MUST** be in the spool name in Filament Manager.
  - Example: If the QR Code ID is 11, 11 must be in the name in Filament Manager
    - **VALID**: QR: `11`, Spool Name: `011 - Black PLA`
    - **INVALID**: QR: `11`, Spool Name: `Black PLA`
- A sheet of labels with IDs 1-30 is included (`label.png`). This is meant to be printed on Avery 5160 Address Labels and applied to each spool. 
  - If you wish to make more labels, use the `label_maker.py` program. Change the `startID` to whatever ID you want. It will generate a new `label.png` image that you can then print.
- If you do not want to use the included label maker, the format for the QR code text payload is `SPOOL - # - SPOOL`. 
  - Replace the `#` with whatever spool ID you have in the name in Filament Manager.
  - A number MUST be between the dashes in the payload of the QR code
  
## Install Steps
1. `$ cd && git clone https://github.com/bwees/FilaScanner && cd FilaScanner`
2. Open `filascanner.py` and set `API_KEY` to the OctoPrint API Key 
2. `$ sudo apt install libzbar0`
3. `$ sudo pip3 install pyzbar pillow pyqrcode`
3. Open `/etc/systemd/system/filascanner.service` in your favorite text editor (ie. nano)
4. Set the contents of the file to:

```
[Unit]
Description=FilaScanner Service
After=multi-user.target
[Service]
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/bin/python3 /home/pi/FilaScanner/filascanner.py
[Install]
WantedBy=multi-user.target
```
5. `$ sudo systemctl daemon-reload && sudo systemctl enable filascanner.service && sudo systemctl start filascanner.service`
6. Place a valid QR code label in front of the octoprint webcam with your printer connected. Printer will beep and show a message on the display.
