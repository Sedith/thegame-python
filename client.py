import zmq
from math import log10


class GameBoard:
    board = []
    deck_size = ''
    hand = []

    def __init__(self, pseudo):
        self.you = pseudo

    def display_board(self):
        print()
        print('----------------------------------')
        print(
            'v',
            ' ' * int(log10(self.board[0])),
            ' v',
            ' ' * int(log10(self.board[1])),
            ' ʌ',
            ' ' * int(log10(self.board[2])),
            ' ʌ',
            sep='',
        )
        print(
            self.board[0], self.board[1], self.board[2], self.board[3],
        )
        print()

    def display_hand(self):
        for card in self.hand:
            print(card, end=' ')
        print()

    def display_score(score):
        print('----------------------------------')
        print('Final score :', score)
        if score == 0:
            print('Congratulations!! :D')
        else:
            print('Maybe next time ;)')


### MAIN
if __name__ == '__main__':
    print('Welcome to ConoraTheGame ^o^')

    context = zmq.Context()
    req_socket = context.socket(zmq.REQ)
    req_socket.connect('tcp://localhost:5555')
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5556")


    # Registration
    while True:
        table = GameBoard(input('What\'s your name? '))
        req_socket.send_json({'method': 'connect', 'pseudo': table.you, 'args': []})
        resp = req_socket.recv_json()
        if resp['status'] == 'error':
            print('Oops, %s' % resp['value'])
        else:
            print('You are in The Game!')
            break

    # Preparation
    print(press)
    print('Ok, here\' your hand:')
    table.display_hand()
    while True:
        prompt = 'In which order would you like to play? '
        req_socket.send_json({'method': 'order', 'pseudo': table.you, 'args': [input(prompt)]})
        resp = req_socket.recv_json()
        if resp['status'] == 'error':
            print('Oops, %s' % resp['value'])
        else:
            print('Got it.')
            break

    # Actual game
    while True:
        # Wait for notification
        notif = sub_socket.recv_json()

        # Update table
        if notif['status'] == end:
            table.display_score()
            exit()
        table.board = notif['board']
        table.deck = notif['deck']
        table.display_board()
        table.display_hand()

        # Check for your turn
        if notif['player'] == table.you:
            tokens = input('action : ').split()
            req_socket.send_json(
                {'pseudo': table.you, 'method': tokens[0], 'args': tokens[1:]}
            )
            resp = req_socket.recv_json()
            if resp['status'] == 'error':
                print('Oops, %s' % resp['value'])
            elif tokens[0] in ['play', 'draw']:
                table.hand = resp['value']
        else:
            print('Waiting for %s to play' % notif['player'])
