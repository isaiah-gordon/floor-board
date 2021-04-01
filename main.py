import eel
import time
import json
import requests
from gameMaster import gameMaster
import socket_master
from datetime import datetime, timedelta

print('FLOOR BOARD')
print('Version 0.4.1\n')

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()


def initialize_frontend():
    # Initiate eel using "frontend" folder.
    eel.init("frontend")
    # Show "main.html" in eel window.
    eel.start("main.html", block=False, cmdline_args=['--start-fullscreen'])
    # Give eel 2 seconds to render "main.html"
    eel.sleep(10.0)


def check_connection(address):
    try:
        requests.get(address, timeout=5)
        return True

    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


initialize_frontend()
socket_master.connect(config['dotops_token'], config['store_number'])

sleep_start = datetime(2021, 1, 1, 23, 00).time()
sleep_end = datetime(2021, 1, 1, 12, 00).time()

while True:

    eel.sleep(1)

    if socket_master.control_dict['status'] != 'idle':

        gameMaster.start_game(socket_master.control_dict, 55, config)

        gameMaster.show_results(2400)

        gameMaster.transition(
            load_file='idle/idle.html',
            title_text='',
            subtitle_text='',
            footer_text="""
            🌐 &nbsp Go to <b>dotops.app</b> to configure an upsell game! &nbsp &nbsp 📁 &nbsp Version 0.4.1
            """)

    time_now = datetime.now().time()
    if sleep_start < time_now < sleep_end:
        print('Hello')


