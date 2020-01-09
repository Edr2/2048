import random


def get_random_24():
    chance = random.randint(1, 100)
    if chance <= 90:
        return 2
    return 4


class Board:
    def __init__(self, width):
        self.width = width
        self.board = [[0 for x in range(width)] for y in range(width)]

        # self.board = [
        #     [8, 4, 2, 4],
        #     [1024, 32, 16, 2],
        #     [16, 2, 64, 8],
        #     [8, 0, 0, 1024],
        # ]

        self.board = Board.fill_zeros(self.board)
        self.board = Board.fill_zeros(self.board)

    @staticmethod
    def get_zeros_tiles(board):
        zeros_indexes = []
        for row_i, row in enumerate(board):
            for i, v in enumerate(row):
                if v == 0:
                    zeros_indexes.append((row_i, i))

        return zeros_indexes

    @staticmethod
    def fill_zeros(board, zeros_indexes=False):
        if not zeros_indexes:
            zeros_indexes = Board.get_zeros_tiles(board)

        if len(zeros_indexes) == 0:
            return board

        rand_zero = random.choice(zeros_indexes)
        (row_i, tile_i) = rand_zero
        board[row_i][tile_i] = get_random_24()

        return board

    def __str__(self):
        output = ''

        for row in self.board:
            row_output = ''
            for tile in row:
                row_output += str(tile) + ' '

            output += row_output + '\n'

        return output

    def move(self, action, check=False):
        reverse = False
        rotated = False

        board = self.board[::]
        old_board = board[::]

        if action == 'move_right' or action == 'move_down':
            reverse = True

        if action == 'move_up' or action == 'move_down':
            board = self.rotate(board)
            rotated = True

        for row_i, row in enumerate(board):
            row = self.zero_move(row)
            for tile_i, tile_v in enumerate(row):
                if tile_i == len(row)-1:
                    continue

                if tile_v and row[tile_i+1] == tile_v:
                    row[tile_i] *= 2
                    row[tile_i+1] = 0
                    if row[tile_i] == 2048:
                        return True

            board[row_i] = self.zero_move(row, reverse)

        if rotated:
            board = self.rotate(board)

        if check:
            return board

        zeros_tiles = Board.get_zeros_tiles(board)
        if not zeros_tiles:
            moves = ['move_left', 'move_right', 'move_up', 'move_down']
            old_board = board
            end_game = True
            for move in moves:
                new_board = self.move(move, check=True)
                result = Board.diff_boards(new_board, old_board)
                if result:
                    end_game = False
                    break

            if end_game:
                return False

        if not Board.diff_boards(old_board, board):
            return board

        self.board = Board.fill_zeros(board)
        return self.board

    @staticmethod
    def diff_boards(new_board, old_board):
        new_board = [i for row in new_board for i in row]
        old_board = [i for row in old_board for i in row]

        return not new_board == old_board

    def rotate(self, board):
        board = [list(row) for row in list(zip(*board))]
        return board

    def zero_move(self, row, left=False):
        only_vals = [i for i in row if i != 0]
        zeros_missing = self.width - len(only_vals)

        if left:
            return zeros_missing * [0] + only_vals
        return only_vals + zeros_missing * [0]
