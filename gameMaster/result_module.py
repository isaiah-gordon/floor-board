import eel


def process_results(product, results):

    sections = {'Lane 1': results[0], 'Lane 2': results[1], 'Counter': results[2]}

    order_sections = sorted(sections, key=sections.get, reverse=True)

    count = 1
    spec_dict = {}
    first_place_tie = False

    for section in order_sections:
        if sections[section] == max(results):
            if results.count(sections[section]) > 2:
                spec_dict[count] = ['second_container', 'TIE', 'images/second_' + product + '.png', section, sections[section]]
                first_place_tie = True
            elif results.count(sections[section]) > 1:
                spec_dict[count] = ['first_container', 'TIE', 'images/first_' + product + '.png', section, sections[section]]
                first_place_tie = True
            else:
                spec_dict[count] = ['first_container', 'FIRST', 'images/first_' + product + '.png', section, sections[section]]

        elif sections[section] != min(results) or first_place_tie == True:
            spec_dict[count] = ['second_container', 'SECOND', 'images/second_' + product + '.png', section, sections[section]]

        else:
            if results.count(sections[section]) > 1:
                spec_dict[count] = ['second_container', 'TIE', 'images/second_' + product + '.png', section, sections[section]]
            else:
                spec_dict[count] = ['third_container', 'THIRD', 'images/third_' + product + '.png', section, sections[section]]

        count += 1

    eel.display_results(spec_dict)


def process_external_results(product, results):

    sections = {'Lane 1': results[0], 'Lane 2': results[1], 'Counter': results[2]}

    order_sections = sorted(sections, key=sections.get, reverse=True)

    count = 1
    spec_dict = {}
    first_place_tie = False

    for section in order_sections:
        if sections[section] == max(results):
            if results.count(sections[section]) > 2:
                spec_dict[count] = ['second_container', 'TIE', 'images/second_' + product + '.png', section, sections[section]]
                first_place_tie = True
            elif results.count(sections[section]) > 1:
                spec_dict[count] = ['first_container', 'TIE', 'images/first_' + product + '.png', section, sections[section]]
                first_place_tie = True
            else:
                spec_dict[count] = ['first_container', 'FIRST', 'images/first_' + product + '.png', section, sections[section]]

        elif sections[section] != min(results) or first_place_tie == True:
            spec_dict[count] = ['second_container', 'SECOND', 'images/second_' + product + '.png', section, sections[section]]

        else:
            if results.count(sections[section]) > 1:
                spec_dict[count] = ['second_container', 'TIE', 'images/second_' + product + '.png', section, sections[section]]
            else:
                spec_dict[count] = ['third_container', 'THIRD', 'images/third_' + product + '.png', section, sections[section]]

        count += 1

    eel.display_results(spec_dict)
