import eel
import json
from gameMaster import gameMaster, result_module, product_catalog
import api_master as api
from datetime import datetime

print('FLOOR BOARD')
print('Version 0.5.5\n')

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


def start_config_idle_type():
    if config['idle_type'] == "covid_safety":
        gameMaster.transition(
            load_file='idle/covid_safety.html',
            title_text='',
            subtitle_text='',
            footer_text='Help prevent the spread of <b>COVID-19</b> and protect others. &#x1F637;',
            product_banner='covid_safety')
    else:
        gameMaster.transition(
            load_file='idle/idle.html',
            title_text='',
            subtitle_text='',
            footer_text='&#128194; Version 0.5.5',
            product_banner='')


initialize_frontend()
start_config_idle_type()

while True:

    try:
        current_time = datetime.utcnow()

        # If it's the middle of the night: go idle for 4 hours.
        if current_time.replace(hour=2) < current_time < current_time.replace(hour=4):
            start_config_idle_type()
            eel.sleep(14400)

        active_game = False

        current_game = api.make_request('find_game/current')
        next_game = api.make_request('find_game/next')
        print('Next game: ', next_game)

        current_time = datetime.utcnow()

        if current_game:
            active_game = current_game

        elif next_game:

            start_time = datetime.strptime(next_game['start_time'], '%H:%M:%S')
            start_time = start_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            print('Next start time: ', start_time)

            eel.sleep((start_time - current_time).total_seconds())

            active_game = next_game

        else:
            eel.sleep(3600)

        if active_game:

            store_info = api.make_request('lookup_stores/{0}'.format(active_game['stores']))

            result = gameMaster.start_game(active_game, store_info, 50, config)

            gameMaster.transition(
                'results/external_results.html',
                'GAME OVER!',
                product_catalog.catalog[active_game['product']]['names']['upper'] + ' upsell results:',
                '???? Winner has the highest <b>U/100</b> &nbsp | &nbsp &#128161; <b>U/100</b> is the amount of product sold for every 100 guests',
                '')

            result_module.process_external_results(
                local_store=config['store_number'],
                stores_list=active_game['stores'],
                store_info=store_info,
                total_sold=result[0],
                transactions=result[1]
            )

    except Exception as e:
        print('EXCEPTION ERROR: ')
        print(e)

        gameMaster.transition(
            load_file='idle/idle.html',
            title_text='',
            subtitle_text='',
            footer_text='&#128565; <b>An ERROR occurred!</b> &nbsp&nbsp Attempting a recovery...',
            product_banner='')

        eel.processProgress('refresh-bar-fill')

        eel.sleep(120)
