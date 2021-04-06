import requests
import xml.dom.minidom
import socketio
import time

# sio = socketio.Client()


def login(address, username, password):
    URL = address
    LOGIN_ROUTE = 'Account/LogOn?ReturnUrl=%2f'

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                             '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
               'Origin': URL, 'Referer': URL + LOGIN_ROUTE}

    s = requests.session()

    login_payload = {
        'UserName': username,
        'Password': password
    }

    login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)

    cookies = login_req.cookies

    return s


def download(address, session, file_name, start_date_time, end_date_time):

    start_date = start_date_time.strftime('%Y-%m-%d')
    start_hour = start_date_time.strftime('%H')
    start_minute = start_date_time.strftime('%M')

    end_date = end_date_time.strftime('%Y-%m-%d')
    end_hour = end_date_time.strftime('%H')
    end_minute = end_date_time.strftime('%M')

    # BUG ALERT!
    # This Ip is not dynamic! Lookout! This will crash at new stores!
    re = session.get(
        address + 'receipts/export?fromDate='+start_date + 'T' + start_hour + '%3A'+start_minute +
        '%3A36.148&toDate=' + end_date + 'T'+end_hour + '%3A'+end_minute + '%3A36.148&posId=&tenderld=&getViews=true'
    )

    download_content = re.content
    download_content = download_content.decode('latin-1')

    xml_download = open(file_name+'.xml', 'w')
    n = xml_download.write(str(download_content))
    xml_download.close()


def count(file_name, product_code_index, id_exclusion_index, level_exclusion):

    exclude = []
    id_index = []
    transaction_amount = {'lane1': 0, 'lane2': 0, 'counter': 0}

    doc = xml.dom.minidom.parse(file_name+'.xml')

    receipts = doc.getElementsByTagName('View')

    result_dict = {'lane1': 0, 'lane2': 0, 'counter': 0}

    for receipt in receipts:

        items = receipt.getElementsByTagName('ItemView')
        cod = receipt.getElementsByTagName('COD')

        if receipt.attributes['uniqueId'].value in id_exclusion_index:
            continue
        elif receipt.attributes['uniqueId'].value not in id_exclusion_index:
            id_index.append(receipt.attributes['uniqueId'].value)

            try:
                if cod[0].getAttribute('number') == '1':
                    transaction_amount['lane1'] += 1

                elif cod[0].getAttribute('number') == '2':
                    transaction_amount['lane2'] += 1

            except IndexError:
                transaction_amount['counter'] += 1

        current_item_code = '0'
        parent_quantity = 1
        for item in items:
            product_code = item.getElementsByTagName('productCode')[0].firstChild.nodeValue
            level = item.getElementsByTagName('level')[0].firstChild.nodeValue
            item_code = item.getElementsByTagName('itemCode')[0].firstChild.nodeValue
            quantity = item.getElementsByTagName('quantity')[0].firstChild.nodeValue

            if level == '0':
                current_item_code = item_code
                parent_quantity = int(quantity)

            elif item_code == current_item_code:
                quantity = int(quantity) * parent_quantity

            if product_code in product_code_index:

                if level == '1' and level_exclusion:
                    continue

                else:
                    x = (int(quantity))
                    y = (int(product_code_index[product_code]))
                    try:
                        if cod[0].getAttribute('number') == '1':
                            result_dict['lane1'] += (x * y)

                        elif cod[0].getAttribute('number') == '2':
                            result_dict['lane2'] += (x * y)

                    except IndexError:
                        result_dict['counter'] += (x * y)

    return result_dict, id_index, transaction_amount
