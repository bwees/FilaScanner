import requests
from PIL import Image
from pyzbar import pyzbar
import time
import re
import json

API_KEY = "<insert key here>"

def change_spool(spool_id, spool_num):

    if send_beeps():
        payload = {"selection":{"tool":0,"spool":{"id":spool_id}}}
        headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
        r = requests.patch('http://localhost/plugin/filamentmanager/selections/0', json=payload, headers=headers)
        
        set_display_message(spool_num)
    else: 
        print("Printer is not on!")


def lookup_id(spool_name_id):
    headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
    r = requests.get('http://localhost/plugin/filamentmanager/spools', headers=headers)
    spools = json.loads(r.text)["spools"]
    spools = [x["id"] for x in spools if str(spool_name_id) in x["name"]]

    if len(spools) > 0:
        return spools[0]

def send_beeps():
    payload = {
        "commands": [
            "M300 S440 P50", "M300 S660 P50", 
        ],
        "parameters": {}
    }
    headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
    r = requests.post('http://localhost/api/printer/command', json=payload, headers=headers)

    return "error" not in r.text

def set_display_message(spool_id):
    msg = "Loaded Spool: #" + str(spool_id)
    payload = {
        "commands": [
            "M117 " + msg, 
        ],
        "parameters": {}
    }
    headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
    r = requests.post('http://localhost/api/printer/command', json=payload, headers=headers)

def get_current_spool():
    headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
    r = requests.get('http://localhost/plugin/filamentmanager/selections', headers=headers)
    return json.loads(r.text)["selections"][0]["spool"]["id"]

pattern = re.compile(r"SPOOL - [0-9]+ - SPOOL")

while True:
    im = Image.open(requests.get("http://localhost:8080/?action=snapshot", stream=True).raw)
    detectedBarcodes = pyzbar.decode(im)

    for code in detectedBarcodes:
        text = str(code.data)
        if pattern.match(text, re.IGNORECASE) != None:
            spool_num = int(text.split(" - ")[1])
            spool_id = lookup_id(spool_num)
            if spool_id != get_current_spool():
                print("Swapping Spool to #" + str(spool_num))
                change_spool(int(spool_id), spool_num)

    time.sleep(1)
