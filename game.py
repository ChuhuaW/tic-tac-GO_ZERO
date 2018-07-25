#implementation structure is forked from fbora/tic-tac-GO_ZERO


import numpy as np
import board

class Game():

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = board.Board()

    def reset(self):
        self.current_player = self.player1
        self.board.reset()

    def next(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def run(self):
        self.reset()
        game_states = [self.board.board.copy()]
        # the starting player always has 'x' (i.e. 1)
        self.player1.type = 1

        #self.player2.type = -1
        # both player uses 'x'
        self.player2.type = 1
        winner = 0
        while not self.board.full():
            move = self.current_player.turn(self.board)
            self.board.add_move(*move)
            game_states.append(self.board.board.copy())
            if board.Board.winner(self.board.board):
                #winner = self.current_player.type
                if self.current_player == self.player1:
                    winner = -1
                    break
                else:
                    winner = 1
                    break
            self.next()
        return [game_states, winner]

    def play(self, N):
        result = []
        print('number of play:', N)
        for game in range(N):
            #print('number of play:', game)
            result.append(self.run())
        return result

    def play_symmetric(self, N):
        player1_first = np.array([x[1] for x in self.play(N//2)])
        #print('player1_first:',player1_first)
        #swap players
        self.player1, self.player2 = self.player2, self.player1
        player1_second = np.array([x[1] for x in self.play(N//2)])
        #print('player1_second:',player1_second)
        win1 = (player1_first == 1).sum() + (player1_second == -1).sum()
        win2 = (player1_first == -1).sum() + (player1_second == 1).sum()

        #win1 = (player1_first == self.player1).sum() + (player1_second == self.player2).sum()
        print('win1:',win1)

        #win2 = (player1_first == self.player2).sum() + (player1_second == self.player1).sum()
        print('win2:',win2)
        return win1, win2





def main():
    print('')

if __name__ == '__main__':
    main()
