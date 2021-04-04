import requests
import json

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()


def make_request(endpoint):
    url = 'https://dotops.app/api/{0}'.format(endpoint)
    token_header = {'token': config['dotops_token']}

    r = requests.get(url, headers=token_header)

    if not r.text:
        return False

    json_dict = json.loads(r.text)
    return json_dict


def lookup_stores(store_index):
    store_data = make_request('lookup_stores/{0}'.format(store_index))
    return store_data


def add_score(game_id, index, total_sold, transactions):
    url = 'https://dotops.app/api/add_score/{0}'.format(game_id)
    token_header = {'token': config['dotops_token']}

    score_dict = {'score_index': index,'total_sold': total_sold, 'transactions': transactions}

    r = requests.post(url, headers=token_header, json=score_dict)


print(make_request('get_score/2'))
