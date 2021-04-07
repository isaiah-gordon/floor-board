import requests
import json
import time
import eel

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()


def safe_request(method, *args, **kwargs):

    try:
        r = requests.request(method, *args, **kwargs)

    except requests.exceptions.ConnectionError:
        request_connection = False
        normal_footer = eel.get_header('footer')
        eel.updateHeader('footer', '&#x1F4E1; &nbsp <b>Connection Error!</b> &nbsp&nbsp Trying to reconnect...')
        while request_connection is False:
            try:
                r = requests.request(method, *args, **kwargs)
                request_connection = True

            except requests.exceptions.ConnectionError:
                print('not connected!')
                time.sleep(10)

        eel.updateHeader('footer', normal_footer)

    return r


def make_request(endpoint):
    url = 'https://dotops.app/api/{0}'.format(endpoint)
    token_header = {'token': config['dotops_token']}

    # r = requests.get(url, headers=token_header)
    r = safe_request('GET', url, headers=token_header)

    if not r.text:
        return None

    json_dict = json.loads(r.text)
    return json_dict


def lookup_stores(store_index):
    store_data = make_request('lookup_stores/{0}'.format(store_index))
    return store_data


def add_score(game_id, index, total_sold, transactions):
    url = 'https://dotops.app/api/add_score/{0}'.format(game_id)
    token_header = {'token': config['dotops_token']}

    score_dict = {'score_index': index,'total_sold': total_sold, 'transactions': transactions}

    # requests.post(url, headers=token_header, json=score_dict)
    safe_request('POST', url, headers=token_header, json=score_dict)

    return True
