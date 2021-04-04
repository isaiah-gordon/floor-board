import eel
from datetime import datetime, timedelta, date
import time
from . import result_module
from gameMaster import product_catalog as pc
import receiptMaster as rm
# import socket_master
import api_master as api


# This function can update one of the two headers in "main.html" based on ID ('title' or 'subtitle')
@eel.expose
def update_header(text_id, text):
    eel.updateHeader(text_id, text)


# This function can add custom names to the upsell scoreboard
# @eel.expose
def add_names(name1, name2, name3):
    eel.addNames(name1, name2, name3)


# This function condenses three eel functions often used in tandem.
def transition(load_file, title_text, subtitle_text, footer_text, product_banner):
    eel.updateHeader('title', title_text)
    eel.updateHeader('subtitle', subtitle_text)
    eel.updateHeader('footer', footer_text)
    eel.load(load_file)
    eel.updateHeader('banner', 'banners/{0}.png'.format(product_banner))
    eel.sleep(1)


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


def sync_second(target_second):
    second_now = datetime.now().second
    wait = target_second - second_now
    if second_now > target_second:
        wait += 60
    time.sleep(wait)


def start_game(game_info, store_info, refresh_seconds, store_config):

    local_index = game_info['stores'].index(store_config['store_number'])

    if len(game_info['stores']) == 2:
        counters_template = 'dual_counters'
    else:
        counters_template = 'counters'

    # Transition to the integrated_counters frontend template. It's basically the scoreboard.
    transition('integrated_counters/{0}.html'.format(counters_template),
               '',
               '',
               pc.catalog[game_info['product']]['footer'],
               game_info['product']
               )

    # If the server has provided names for the players: add them to the scoreboard.

    store_names = []
    for store in game_info['stores']:
        store_names.append(store_info[store]['store_short_name'])

    if len(store_names) == 2:
        store_names.append('')

    add_names(*store_names)

    eel.sleep(2)

    obj_end_time = datetime.strptime(game_info['end_time'], '%H:%M:%S').time()
    now = datetime.utcnow().time()
    seconds_until_end = round((datetime.combine(date.min, obj_end_time) - datetime.combine(date.min, now)).total_seconds())

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

    previous_external_result = {}

    for store in game_info['stores']:
        previous_external_result.update({store: 0})

    gain_sold = {}

    last_sold = {'total_sold0': 0, 'total_sold1': 0, 'total_sold2': 0, }
    last_transactions = {}

    while True:
        eel.processProgress('refresh-bar-fill')

        now = datetime.now()
        start = now - fiveMinute
        end = now

        # Use the receiptMaster module to retrieve data based on var "start" and var "end"
        rm.download(store_config['rmu_address'], session, 'moduleDownload', start, end)

        # Use the receiptMaster module to count how many products each area has sold based on product dictionaries.
        # The exclusion list is used here to prevent receiptMaster from reading receipts from the last count.
        raw_result = rm.count(
            'moduleDownload',
            pc.catalog[game_info['product']]['codes'],
            exclusion,
            pc.catalog[game_info['product']]['level_exclusion']
        )

        # Assign var "result" to the first return from raw_result.
        # The first return is a dictionary of the count results ( e.g. {'lane1': 10, 'lane2': 5, 'counter': 2} )
        result = raw_result[0]

        # Append the second return from raw_result to the "exclusion" list.
        # The second return is a list of receipt IDs that were read.
        exclusion += raw_result[1]

        #   - - - EXTERNAL GAME - - -
        #   Store Vs Store
        #   Only type of game as of version 0.5.0

        local_sold = sum(raw_result[0].values())
        local_transactions = sum(raw_result[2].values())

        sync_second(0)

        api.add_score(game_info['id'], local_index, local_sold, local_transactions)

        sync_second(3)

        latest_scores = api.make_request('get_score/{0}'.format(game_info['id']))

        latest_sold = {}
        latest_transactions = {}
        for score in latest_scores:
            if 'transaction' in score:
                latest_transactions[score] = latest_scores[score]
                continue
            latest_sold[score] = latest_scores[score]

        for result in latest_sold:
            gain_sold[result] = latest_sold[result] - last_sold[result]

        last_sold = latest_sold

        # total_gained_result = {}
        # for result in latest_external_result:
        #     gain = latest_external_result[result] - previous_external_result[result]
        #     total_gained_result.update({result: gain})
        #
        # previous_external_result.update(latest_external_result)

        # This while loop adds donuts to each section based on the "result" dictionary until all have been added.
        addon_count = 0
        while True:
            store_count = 0
            for result in latest_sold:

                if addon_count < gain_sold[result]:
                    eel.product_add(game_info['product'], store_count, 1)
                store_count += 1

            if addon_count >= max(latest_sold.values()):
                break

            addon_count += 1
            eel.sleep(0.6)

        section_index_count = 0
        for result in latest_transactions:

            if section_index_count == 2 and len(game_info['stores']) == 2:
                continue

            try:
                average = (latest_sold['total_sold{0}'.format(section_index_count)] / latest_transactions[result]) * 100

            except ZeroDivisionError:
                average = 0

            eel.update_average(str(section_index_count), (str(round(average, 1)) + '%'))
            section_index_count += 1

            eel.sleep(0.2)

        eel.resetProgress('refresh-bar-fill')
        eel.sleep(1.0)

        # This should properly end games at the desired time. (Version 0.5.0)
        if check_end_time(game_info['end_time']):
            return [latest_sold, latest_transactions]

        # Run the refresh progress bar for a desired amount of seconds.

        second_now = datetime.now().second
        wait_seconds = 50 - second_now

        eel.startProgress('refresh-bar-fill', wait_seconds)

        time.sleep(wait_seconds)


def process_external_results(show_seconds_amount, game_info, store_info):
    eel.resetProgress('refresh-bar-fill')

    results = eel.get_results()()

    transition('results/external_results.html',
               'GAME OVER!',
               pc.catalog[game_info['product']]['names']['upper'] + ' upsell results:',
               '🏆 The results are in!',
               '')

    result_module.process_external_results(game_info['product'], results)
    eel.sleep(5)

    time.sleep(show_seconds_amount)
