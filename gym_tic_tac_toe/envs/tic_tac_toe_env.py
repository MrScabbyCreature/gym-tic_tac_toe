from gym import Env
from itertools import product
import random

PLAYER1 = 'X'
PLAYER2 = 'O'
EMPTY = ' '

class CustomSpace():
    '''
    The spaces avaliable in gym did not work for this case.
    This is a custom space class to handle the action and observation spaces
    for tic-tac-toe.
    '''
    def __init__(self, listy):
        self.n = len(listy)
        self.listy = listy

    def sample(self):
        if isinstance(self.listy, list):
            return random.choice(self.listy)

    def contains(self, x):
        return x in self.listy

    def __repr__(self):
        return str(self.listy)

def check_state_validity(state):
    '''
    # returns if current state is valid.
    '''
    count = 0
    for i in state:
        if i == PLAYER1:
            count += 1
        elif i == PLAYER2:
            count -= 1
    if count in [-1, 0, 1]:
        return True
    return False

def turn(state):
    '''
    given the state, returns whose turn it is.
    '''
    count = 0
    for i in state:
        if i == PLAYER1:
            count += 1
        elif i == PLAYER2:
            count -= 1
    if count == 1:
        return PLAYER2
    return PLAYER1

def check_game_state(state):
    '''
    returns done(bool), player_win(bool))
    '''
    # a player has won
    for t in [PLAYER1, PLAYER2]:
        for index in range(0, 3):
            # rows
            if state[index*3] == t and state[index*3+1] == t and state[index*3 + 2] == t:
                return True, True

            # columns
            if state[index] == t and state[index+3] == t and state[index+6] == t:
                return True, True

        # diagonals
        if state[0] == t and state[4] == t and state[8] == t:
            return True, True
        if state[2] == t and state[4] == t and state[6] == t:
            return True, True

    # draw
    for i in state:
        if i == EMPTY:
            return False, False
    return True, False

class TicTacToeEnv(Env):
    """
    TicTacToe Game:
        3x3 Table
        Player X starts first by default

    Observations:
        3^9 states possible

    Actions:
    There are 9 discrete deterministic actions per player (2 Players). Total actions are 18

    Rewards:
    # Winning - +1
    Losing  - -1
    Draw    - 0
    Invalid - -100
    """
    metadata = {'render.modes': ['human']}


    def __init__(self):
        #calculating the P table
        options = [PLAYER1, PLAYER2, EMPTY]
        pos_combs = product(options, options, options, options, options, options, options, options, options)
        self.P = {}

        for state in pos_combs:
            valid = check_state_validity(state)
            if not valid:
                continue
            self.P[state] = {}
            player = turn(state)
            for action_pos in range(9):
                next_state = list(state)
                next_state[action_pos] = player
                done, player_win = check_game_state(next_state)

                if state[action_pos] != EMPTY:
                    self.P[state][action_pos] = [1.0, state, -100, False]
                else:
                    if player_win:
                        reward = 1
                    else:
                        reward = 0
                    self.P[state][action_pos] = [1.0, tuple(next_state), reward, check_game_state(next_state)[0]]

        # setting up our spaces
        self.action_space = CustomSpace([action_pos for action_pos in range(9)])
        self.observation_space = CustomSpace(list(self.P.keys()))

        # initialize and start play
        self.reset()

    def step(self, a):
        if self.action_space.contains(a):
            p, s, r, d= self.P[self.s][a]
            self.s = s
            return (s, r, d, {"turn": turn(s)})
        else:
            print("Invalid Move")

    def reset(self):
        self.s = (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY)
        return self.s

    def render(self, mode='human', close=False):
        print("\t {} | {} | {}".format(self.s[0], self.s[1], self.s[2]))
        print("\t-----------")
        print("\t {} | {} | {}".format(self.s[3], self.s[4], self.s[5]))
        print("\t-----------")
        print("\t {} | {} | {}".format(self.s[6], self.s[7], self.s[8]))


if __name__ == '__main__':
    env = TicTacToeEnv()
