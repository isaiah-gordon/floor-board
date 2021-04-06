import eel


def process_external_results(local_store, stores_list, store_info, total_sold, transactions):

    averages = {}
    averages_list = []
    for idx, result in enumerate(total_sold):

        if len(stores_list) == 2 and idx == 2:
            continue

        try:
            average = (total_sold[result] / transactions['transactions{0}'.format(idx)]) * 100
        except ZeroDivisionError:
            average = 0

        averages[stores_list[idx]] = average
        averages_list.append(average)

    store_names = []
    for store in store_info:
        store_names.append(store_info[store]['store_name'])

    descending_averages = sorted(averages, key=averages.get, reverse=True)

    count = 1
    spec_dict = {}
    first_place_tie = False

    for idx, store in enumerate(descending_averages):

        highlight = False
        if local_store == store:
            highlight = True

        store_data = [
            store_info[store]['store_name'],
            store_info[store]['store_image'],
            total_sold['total_sold{0}'.format(stores_list.index(store))],
            str(round(averages[store], 2)) + '%',
            highlight
        ]

        if averages[store] == max(averages.values()):
            if averages_list.count(averages[store]) > 2:
                spec_dict[count] = ['TIE']
                first_place_tie = True
            elif averages_list.count(averages[store]) > 1:
                spec_dict[count] = ['TIE']
                first_place_tie = True
            else:
                spec_dict[count] = ['1<sup>st</sup>']

        elif averages[store] != min(averages.values()) and averages[store] != max(averages.values()):
            spec_dict[count] = ['2<sup>nd</sup>']

        elif averages[store] == min(averages.values()) and len(averages) == 2:
            spec_dict[count] = ['2<sup>nd</sup>']

        else:
            if averages_list.count(averages[store]) > 1:
                spec_dict[count] = ['TIE']
            else:
                spec_dict[count] = ['3<sup>rd</sup>']

        spec_dict[count] += store_data
        count += 1

    eel.display_results(spec_dict)
