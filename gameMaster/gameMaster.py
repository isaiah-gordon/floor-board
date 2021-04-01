import eel
from datetime import datetime, timedelta, date
import time
from . import product_catalog, counter_module, result_module
from gameMaster import product_catalog as pc
import receiptMaster as rm
import socketio as sio
import socket_master


# This function can update one of the two headers in "main.html" based on ID ('title' or 'subtitle')
@eel.expose
def update_header(text_id, text):
    eel.updateHeader(text_id, text)


# This function can add custom names to the upsell scoreboard
# @eel.expose
def add_names(name1, name2, name3):
    eel.addNames(name1, name2, name3)


# This function condenses three eel functions often used in tandem.
def transition(load_file, title_text, subtitle_text, footer_text):
    eel.updateHeader('title', title_text)
    eel.updateHeader('subtitle', subtitle_text)
    eel.updateHeader('footer', footer_text)
    eel.load(load_file)
    eel.sleep(3)


# This function can add a certain amount of a certain product to the scoreboard.
def product_add(product, area, amount):
    eel.product_add(product, area, amount)


# Converts string time into datetime obj.
# Returns True if time parameter is less than the current UTC time.
def check_end_time(str_time):
    obj_end_time = datetime.strptime(str_time, '%H:%M:%S').time()

    if obj_end_time <= datetime.utcnow().time():
        return True
    else:
        return False


def start_game(game_specs_dict, refresh_seconds, store_config):

    # Transition to the integrated_counters frontend template. It's basically the scoreboard.
    transition('integrated_counters/{0}.html'.format(socket_master.control_dict['scoreboard_config']),
               pc.catalog[socket_master.control_dict['product']]['names']['upper_plural']+'!',
               'Who can sell the most?',
               pc.catalog[socket_master.control_dict['product']]['footer'])

    # If the server has provided names for the players: add them to the scoreboard.
    if socket_master.control_dict['name1'] and socket_master.control_dict['name2'] != '':
        add_names(socket_master.control_dict['name1'], socket_master.control_dict['name2'], socket_master.control_dict['name3'])

    eel.sleep(2)

    obj_end_time = datetime.strptime(game_specs_dict['end_time'], '%H:%M:%S').time()
    print(obj_end_time)
    now = datetime.utcnow().time()
    print(now)
    seconds_until_end = round((datetime.combine(date.min, obj_end_time) - datetime.combine(date.min, now)).total_seconds())
    print('SECONDS UNTIL END: ', seconds_until_end)

    # Depreciated progress bar. Delete if code runs without errors.
    # eel.startProgress('goal-bar-fill', str(seconds_until_end))

    # Start an RMU session using the receiptMaster module.
    session = rm.login(store_config['rmu_address'], store_config['rmu_username'], store_config['rmu_password'])

    # Create a list to store excluded receipt IDs. This will help prevent the same receipt from being read twice.
    exclusion = []

    # Create a dictionary to store the total transactions for each station. This will help calculate averages.
    transaction_amounts = {'lane1': 0, 'lane2': 0, 'counter': 0}
    total_counts = {'lane1': 0, 'lane2': 0, 'counter': 0}

    # Assign five minute time delta using datetime module.
    fiveMinute = timedelta(minutes=5)

    # End this game function if the server has changed the game status to idle.
    if socket_master.control_dict['status'] == 'idle':
        return True

    previous_external_result = {}

    if game_specs_dict['status'] == 'external_game':
        for store in game_specs_dict['stores_list']:
            previous_external_result.update({store: 0})

    while True:
        eel.processProgress('refresh-bar-fill')

        now = datetime.now()
        start = now - fiveMinute
        end = now

        # Use the receiptMaster module to retrieve data based on var "start" and var "end"
        rm.download(store_config['rmu_address'], session, 'moduleDownload', start, end)

        # Use the receiptMaster module to count how many products each area has sold based on product dictionaries.
        # The exclusion list is used here to prevent receiptMaster from reading receipts from the last count.
        rawResult = rm.count('moduleDownload', pc.catalog[game_specs_dict['product']]['codes'], exclusion, pc.catalog[game_specs_dict['product']]['level_exclusion'])  # TEST HERE ( level_exclusion= )

        # Assign var "result" to the first return from rawResult.
        # The first return is a dictionary of the count results ( e.g. {'lane1': 10, 'lane2': 5, 'counter': 2} )
        result = rawResult[0]

        # Append the second return from rawResult to the "exclusion" list.
        # The second return is a list of receipt IDs that were read.
        exclusion += rawResult[1]

        if socket_master.control_dict['status'] == 'idle':
            return True

        #   - - - INTERNAL GAME - - -
        #   Crew Vs Crew
        #   Scores are retrieved internally and sorted into order taking stations.
        if game_specs_dict['status'] == 'internal_game':

            # --- NEW CODE --- This loop has been rewritten to resolve a drive-thru compatibility bug
            # This while loop adds products to each section based on the "result" dictionary until all have been added.
            addon_count = 0
            while True:
                station_count = 0
                for station in result:
                    if station == 'lane2' and store_config['lane_type'] == 'single':
                        continue

                    if addon_count < result[station]:
                        eel.product_add(game_specs_dict['product'], station_count, 1)
                    station_count += 1

                if addon_count >= max(result.values()):
                    break

                addon_count += 1

                eel.sleep(0.6)

            # --- END OF NEW CODE ---

            latest_transaction_amounts = rawResult[2]

            for station in transaction_amounts:
                transaction_amounts[station] = transaction_amounts[station] + latest_transaction_amounts[station]

            for station in total_counts:
                total_counts[station] = total_counts[station] + result[station]

            # --- NEW CODE --- Being tested

            section_index_count = 0
            for station in total_counts:

                if station == 'lane2' and store_config['lane_type'] == 'single':
                    continue

                try:
                    average = (total_counts[station] / transaction_amounts[station]) * 100

                except ZeroDivisionError:
                    average = 0

                eel.update_average(str(section_index_count), (str(round(average, 1)) + '%'))
                section_index_count += 1

            eel.sleep(0.2)

            # --- END OF NEW CODE ---

        #   - - - EXTERNAL GAME - - -
        #   Store Vs Store
        #   Scores need to be retrieved from the server.
        if game_specs_dict['status'] == 'external_game':

            total_score = {socket_master.store_number: sum(result.values())}
            latest_external_result = socket_master.score_trade(game_specs_dict['external_id'], total_score)
            print('LATEST RESULT', latest_external_result)

            total_gained_result = {}

            for result in latest_external_result:
                gain = latest_external_result[result] - previous_external_result[result]
                total_gained_result.update({result: gain})

            previous_external_result.update(latest_external_result)

            # This while loop adds donuts to each section based on the "result" dictionary until all have been added.
            addon_count = 0
            while True:
                print('TOTAL GAINED:', total_gained_result)
                if addon_count < total_gained_result[game_specs_dict['stores_list'][0]]:
                    eel.product_add(game_specs_dict['product'], 0, 1)

                if addon_count < total_gained_result[game_specs_dict['stores_list'][1]]:
                    eel.product_add(game_specs_dict['product'], 1, 1)

                if game_specs_dict['scoreboard_config'] == 'counters':
                    if addon_count < total_gained_result[game_specs_dict['stores_list'][2]]:
                        eel.product_add(game_specs_dict['product'], 2, 1)

                print('HIGHEST SCORE:', max(total_gained_result.values()))
                print('ADDON COUNT:', addon_count)
                if addon_count >= max(total_gained_result.values()):
                    break

                addon_count += 1

                eel.sleep(0.6)

        eel.resetProgress('refresh-bar-fill')
        eel.sleep(1.0)

        if socket_master.control_dict['status'] == 'idle':
            return True

        # Check to see if the current time matches a desired time to break the game loop.

        # Bugged code:
        # check_end_time(game_specs_dict['end_time'])

        # This should properly end games at the desired time. (Version 0.3.2)
        if check_end_time(game_specs_dict['end_time']):
            socket_master.control_dict['status'] = 'idle'
            return True

        # Run the refresh progress bar for a desired amount of seconds.
        eel.startProgress('refresh-bar-fill', str(refresh_seconds))

        wait_count = 0
        while wait_count != refresh_seconds:
            if socket_master.control_dict['status'] == 'idle':
                return True
            time.sleep(1)
            wait_count += 1


def show_results(show_seconds_amount):
    eel.resetProgress('refresh-bar-fill')

    results = eel.get_results()()

    transition('results/results.html',
               'GAME OVER!',
               pc.catalog[socket_master.control_dict['product']]['names']['upper'] + ' upsell results:',
               '🏆 The results are in!')

    result_module.process_results(socket_master.control_dict['product'], results)
    eel.sleep(5)

    if socket_master.control_dict['status'] != 'idle':
        return True

    count = 0
    while socket_master.control_dict['status'] == 'idle':
        time.sleep(1)
        count += 1
        if count > show_seconds_amount:
            return True
