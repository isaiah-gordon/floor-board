import eel
import time
import json
import requests
from gameMaster import gameMaster, result_module, product_catalog
# import socket_master
import api_master as api
from datetime import datetime, timedelta

print('FLOOR BOARD')
print('Version 0.5.2\n')

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()


def initialize_frontend():
    # Initiate eel using "frontend" folder.
    eel.init("frontend")
    # Show "main.html" in eel window.
    eel.start("main.html", block=False, cmdline_args=['--start-fullscreen'])
    # Give eel 2 seconds to render "main.html"
    eel.sleep(4.0)


initialize_frontend()
# socket_master.connect(config['dotops_token'], config['store_number'])


while True:

    current_time = datetime.utcnow()

    # If it's the middle of the night: go idle for 4 hours.
    if current_time.replace(hour=2) < current_time < current_time.replace(hour=4):
        gameMaster.transition(
            load_file='idle/idle.html',
            title_text='',
            subtitle_text='',
            footer_text='&#128194; Version 0.5.2',
            product_banner='')
        eel.sleep(14400)

    status = False

    next_game = api.make_request('find_next_game')
    print('Next game: ', next_game)

    current_time = datetime.utcnow()

    if next_game:

        start_time = datetime.strptime(next_game['start_time'], '%H:%M:%S')
        start_time = start_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
        print('Next start time: ', start_time)

        eel.sleep((start_time - current_time).total_seconds())

        status = True

    else:
        eel.sleep(3600)

    if status:

        store_info = api.make_request('lookup_stores/{0}'.format(next_game['stores']))

        result = gameMaster.start_game(next_game, store_info, 55, config)

        gameMaster.transition(
            'results/external_results.html',
            'GAME OVER!',
            product_catalog.catalog[next_game['product']]['names']['upper'] + ' upsell results:',
            '🏆 The results are in!',
            '')

        result_module.process_external_results(
            local_store=config['store_number'],
            stores_list=next_game['stores'],
            store_info=store_info,
            total_sold=result[0],
            transactions=result[1]
        )
