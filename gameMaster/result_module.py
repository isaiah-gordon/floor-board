import eel


def process_external_results(local_store, stores_list, store_info, total_sold, transactions):

    scores = {}  # averages
    scores_list = []  # averages_list
    for idx, result in enumerate(total_sold):

        if len(stores_list) == 2 and idx == 2:
            continue

        x = transactions['transactions{0}'.format(idx)]

        scores[stores_list[idx]] = x
        scores_list.append(x)

    store_names = []
    for store in store_info:
        store_names.append(store_info[store]['store_name'])

    descending_scores = sorted(scores, key=scores.get, reverse=True)

    count = 1
    spec_dict = {}
    # first_place_tie = False

    for idx, store in enumerate(descending_scores):

        highlight = False
        if local_store == store:
            highlight = True

        store_data = [
            store_info[store]['store_name'],
            store_info[store]['store_image'],
            str(total_sold['total_sold{0}'.format(stores_list.index(store))]),
            scores[store],
            highlight
        ]

        if scores[store] == max(scores.values()):
            if scores_list.count(scores[store]) > 2:
                spec_dict[count] = ['TIE']
                # first_place_tie = True
            elif scores_list.count(scores[store]) > 1:
                spec_dict[count] = ['TIE']
                # first_place_tie = True
            else:
                spec_dict[count] = ['1<sup>st</sup>']

        elif scores[store] != min(scores.values()) and scores[store] != max(scores.values()):
            spec_dict[count] = ['2<sup>nd</sup>']

        elif scores[store] == min(scores.values()) and len(scores) == 2:
            spec_dict[count] = ['2<sup>nd</sup>']

        else:
            if scores_list.count(scores[store]) > 1:
                spec_dict[count] = ['TIE']
            else:
                spec_dict[count] = ['3<sup>rd</sup>']

        spec_dict[count] += store_data
        count += 1

    eel.display_results(spec_dict)
