import socketio
import datetime

sio = socketio.Client()

control_dict = {'status': 'idle'}
external_scores = {}
store_number = ''


def connect(token, store_number_parm):
    global store_number
    store_number = store_number_parm
    sio.connect('https://dotops.app/socket.io/?token={0}'.format(token))
    # sio.connect('http://127.0.0.1:5000/socket.io/?token={0}'.format(token))
    sio.sleep(seconds=0.02)


@sio.event
def handshake():
    sio.sleep(seconds=0.01)
    print('handshake')
    sio.emit('handshake', {'store_number': store_number, 'status': 'idle'})


@sio.event
def activate(data):
    global control_dict
    print('Received command: ', data)
    control_dict.update(data)

    if control_dict['status'] == 'idle':
        sio.emit('handshake', {'store_number': store_number, 'status': 'idle'})

    if control_dict['status'] == 'internal_game':
        sio.emit('handshake', {'store_number': store_number, 'status': 'internal_game'})
        print('After wait:')
        print(control_dict)

    if control_dict['status'] == 'external_game':
        sio.emit('handshake', {'store_number': store_number, 'status': 'external_game'})
        print('After wait:')
        print(control_dict)


def score_trade(game_id, client_score):
    global external_scores
    sio.emit('score_report', {'game_id': game_id, 'client_score': client_score})
    sio.sleep(seconds=3)
    sio.emit('pull_scores', game_id)
    print('\n\n')
    print(datetime.datetime.now())
    sio.sleep(seconds=2)
    print('SCORE TRADE:', external_scores)
    return external_scores


@sio.event
def receive_game_scores(scores):
    global external_scores
    external_scores.update(scores)

# @sio.on('disconnect')
# def disconnect():
#     print('Reconnecting...')
#     sio.connect('http://127.0.0.1:5000/socket.io/?token={0}'.format(token))
#     sio.sleep(seconds=0.01)
