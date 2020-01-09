from models import Board

permit_keys = {
    'a': 'move_left',
    's': 'move_down',
    'w': 'move_up',
    'd': 'move_right',
    'c': 'break'
}


if __name__ == '__main__':
    board = Board(4)
    print(board)
    while True:
        key = input()

        if key not in permit_keys:
            continue
        if key == 'c':
            break

        status = board.move(permit_keys[key])
        if status is True:
            print('WIN')
            break
        elif status is False:
            print('LOSE')
            break
        print(board)
