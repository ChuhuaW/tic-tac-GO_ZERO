#implementation structure is forked from fbora/tic-tac-GO_ZERO



import os
import numpy as np
import functools

class Board():
    #INT2STR_MAP = {0: ' ', 1: 'x', -1: 'o'}
    #STR2INT_MAP = {' ': 0, 'x': 1, 'o': -1}
    # for reverse tictactoe we only have one symbol 
    INT2STR_MAP = {0: ' ', 1: 'x'}
    STR2INT_MAP = {' ': 0, 'x': 1}
    SIZE = np.array([5, 5])
    WIN_SUM = 5

    def __init__(self):
        self.board = np.zeros(Board.SIZE)

    def reset(self):
        self.board.fill(0)

    def add_move(self, play, row, col):
        if self.board[row, col] != 0:
            raise Exception('invalid move')
        self.board[row, col] = play

    def empty(self):
        return self.board.ravel().astype(bool).sum() == 0

    def full(self):
        return self.board.ravel().astype(bool).sum() == Board.SIZE.prod()

    def display(self, clear=False):
        if clear:
            os.system('cls')
        # print(
        #     '\n'
        #     '\t {0} | {1} | {2}\n'
        #     '\t---+---+---\n'
        #     '\t {3} | {4} | {5}\n'
        #     '\t---+---+---\n'
        #     '\t {6} | {7} | {8}\n\n'.format(
        #         *[Board.INT2STR_MAP[x] for x in self.board.ravel()]))
        # print(
        #     '\n'
        #     '\t {0} | {1} | {2} | {3}\n'
        #     '\t---+---+---+---\n'
        #     '\t {4} | {5} | {6} | {7}\n'
        #     '\t---+---+---+---\n'
        #     '\t {8} | {9} | {10} | {11}\n'
        #     '\t---+---+---+---\n'
        #     '\t {12} | {13} | {14} | {15}\n\n'.format(
        #         *[Board.INT2STR_MAP[x] for x in self.board.ravel()]))
        print(
            '\n'
            '\t {0} | {1} | {2} | {3} | {4}\n'
            '\t---+---+---+---+---\n'
            '\t {5} | {6} | {7} | {8} | {9}\n'
            '\t---+---+---+---+---\n'
            '\t {10} | {11} | {12} | {13} | {14}\n'
            '\t---+---+---+---+---\n'
            '\t {15} | {16} | {17} | {18} | {19}\n'
            '\t---+---+---+---+---\n'
            '\t {20} | {21} | {22} | {23} | {24}\n\n'.format(
                *[Board.INT2STR_MAP[x] for x in self.board.ravel()]))        

    @classmethod
    def arr2str(cls, arr):
        return ''.join(Board.INT2STR_MAP[i] for i in arr.ravel())

    @classmethod
    def str2arr(cls, strmove):
        return np.array([Board.STR2INT_MAP[i] for i in strmove]).reshape(cls.SIZE)

    @classmethod
    def stringmove2int(cls, stringmove):
        init, final = stringmove.split('2')
        idx = [i for i in range(len(init)) if init[i]!=final[i]][0]
        return idx

    @classmethod
    def winner(cls, board):
        '''Returns the winner of the board by checking rows, columns and diagonals'''
        rows = board.sum(axis=1)
        row_winner = np.sign(rows[np.where(np.abs(rows) == Board.WIN_SUM)])
        if len(row_winner)>0:
            return row_winner[0]

        cols = board.sum(axis=0)
        col_winner = np.sign(cols[np.where(np.abs(cols) == Board.WIN_SUM)])
        if len(col_winner) > 0:
            return col_winner[0]

        diag = np.diag(board).sum()
        if abs(diag) == Board.WIN_SUM:
            return np.sign(diag)

        off_diag = np.diag(np.fliplr(board)).sum()
        if abs(off_diag) == Board.WIN_SUM:
            return np.sign(off_diag)

        return 0


    @classmethod
    def generate_state_space(cls):
        def f(i, p, m):
            l = list(p)
            l[i] = m
            return l

        tree = dict()
        edges = list()

        root = cls.SIZE.prod()*' '
        #print("size:",cls.SIZE)
        #print("size prod:",cls.SIZE.prod())
        #print("root:",root)
        parents = [root]
        #print("parents,", parents)
        curr_move = 'x'
        #print(len(root))
        for level in range(3):
            #print("level",level)
            for p in parents:
                #print('p:',p)
                possible_moves = [i for i in range(len(p)) if p[i] == ' ']
                #print("possible_moves:",possible_moves)
                children = set([''.join(f(x, p, curr_move)) for x in possible_moves])
                # print("children",children)
                tree[p] = children
                edges += [p+'2'+c for c in children]
            #print('functools.reduce start')
            parents = functools.reduce(set.union, tree.values())
            #print('functools.reduce end')
            parents = set(parents) - set(tree.keys())
            parents = set([x for x in parents if not cls.winner(cls.str2arr(x))])
            #curr_move = 'x' if curr_move!='x' else 'o'
        edges = set(edges)
        #print("edges:", edges)
        edges_statistics = dict()
        for k in edges:
            edges_statistics[k] = {'N': 0, 'W': 0, 'D': 0, 'L': 0, 'Q': 0, 'P': 0}
        #print(edges_statistics)

        return tree, edges_statistics


def main():
    print('')
    #print(np.zeros(Board.SIZE))
    # board =np.array([[-1.,-1.,1.],[-1.,-1.,0.],[-1.,-1.,0.]])
    # rows = board.sum(axis=0)
    # print('rows:',rows)
    # print(np.where(np.abs(rows)== Board.WIN_SUM))
    # row_winner = np.sign(rows[np.where(np.abs(rows) == Board.WIN_SUM)])
    # print("row_winner:",row_winner)
    # print('length:',len(row_winner))
    # print(row_winner[0])


    # board = Board()
    # board.board = np.array([[-1.,-1.,1.],[-1.,-1.,0.],[-1.,-1.,0.]])
    #print('Board winner',Board.winner(board.board))
if __name__ == '__main__':
    main()
