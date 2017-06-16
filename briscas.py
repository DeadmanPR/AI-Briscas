# Coded by Jose Antonio Rodriguez Rivera
# Using the aima-python libraries

"""The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""Games, or Adversarial Search (Chapter 5)"""

from collections import namedtuple
import random
import copy
import tkinter as tk
from tkinter import messagebox

from utils import argmax

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ______________________________________________________________________________
# Minimax Search


def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  key=lambda a: min_value(game.result(state, a)))

# ______________________________________________________________________________


def alphabeta_full_search(state, game, d=10):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""


    player = game.to_move(state)
    #player = 'A'


    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        #print('MAX DEPTH: ' + str(depth))
        if cutoff_test(state, depth):
            return gameSim.utility(state, player)
        #if gameSim.terminal_test(state):
        #    return gameSim.utility(state, player)
        v = -infinity
        for a in gameSim.actions(state):
            v = max(v, min_value(gameSim.result(state, a), alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        #print('MIN DEPTH: ' + str(depth))
        if cutoff_test(state, depth):
            return gameSim.utility(state, player)

        v = infinity
        for a in gameSim.actions(state):
            v = min(v, max_value(gameSim.result(state, a), alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None

    cutoff_test = (lambda state, depth: depth > d or
                    game.terminal_test(state))
    # MonteCarlo simulation
    for i in range(0, 100):
        gameSim = Briscas()
        deck = copy.deepcopy(state.board['cardsNotPlayed'])
        random.shuffle(deck)
        gameSim.setSimulationCards(state)
        state = copy.deepcopy(state)
        
        for a in gameSim.actions(state):
                

                v = min_value(gameSim.result(state, a), best_score, beta, 0)
                if v > best_score:
                    best_score = v
                    best_action = a

    return best_action


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in gameSim.actions(state):
            v = max(v, min_value(gameSim.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in gameSim.actions(state):
            v = min(v, max_value(gameSim.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    
    gameSim = Briscas()
    deck = copy.deepcopy(state.board['cardsNotPlayed'])
    random.shuffle(deck)
    gameSim.setSimulationCards(state.board['playerAHand'],deck, state.board['trumpCard'])
    state = copy.deepcopy(state)
    
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    """Make a move by querying standard input."""
    print("\n\n\n====================================================================================================\ncurrent state:")
    game.display(state)
    #print("available moves: {}".format(game.actions(state)))
    
    numberOfCards = len(game.actions(state))
    for i in range(0, numberOfCards):
        card = game.actions(state)[i]
        if(i == 0):
            movesStr = str(card[0]) + ' of ' + card[1].upper()
        else:
            movesStr += ']   [' + str(card[0]) + ' of ' + card[1].upper()
            
    print("available moves: [" + movesStr + "]")
    if(numberOfCards == 3):
        print("\t\t     (0)\t\t(1)\t\t(2)")
    elif(numberOfCards == 2):
        print("\t\t     (0)\t\t(1)")
    else:
        print("\t\t     (0)")
        
    print("")

    validInput = False

    while(not validInput):
        if (numberOfCards == 3):
            move_string = input('Your move? [0 for first card, 1 for second card, 2 for third card]: ')
        elif (numberOfCards == 2):
            move_string = input('Your move? [0 for first card, 1 for second card]: ')
        elif (numberOfCards == 1):
            move_string = input('Your move? [0 for first card]: ')

        try:
            index = int(move_string)
           
            
            if(index >= numberOfCards):
                 print('Please choose between the possible moves!')
            else:
                validInput = True
        except ValueError:
            print('Please choose between the possible moves!')
            validInput = False



    move = game.actions(state)[index]

    return move





def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)

#================== Game Class =======================================================

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


#==================================================================================================================================================
class Briscas(Game):

    def __init__(self):
        # Cards definition / instantiation
        self.cards = []
        self.playerAHand = []
        self.playerBHand = []
        self.playerAPoints = 0
        self.playerBPoints = 0

    def initGame(self):
        """Set initial state (player turn, trump, cards in hand)"""

        # Swords
        self.cards.append([1, 'swords', 11])
        self.cards.append([2, 'swords', 0])
        self.cards.append([3, 'swords', 10])
        self.cards.append([4, 'swords', 0])
        self.cards.append([5, 'swords', 0])
        self.cards.append([6, 'swords', 0])
        self.cards.append([7, 'swords', 0])
        self.cards.append([10, 'swords', 2])
        self.cards.append([11, 'swords', 3])
        self.cards.append([12, 'swords', 4])

        # Coins
        self.cards.append([1, 'coins', 11])
        self.cards.append([2, 'coins', 0])
        self.cards.append([3, 'coins', 10])
        self.cards.append([4, 'coins', 0])
        self.cards.append([5, 'coins', 0])
        self.cards.append([6, 'coins', 0])
        self.cards.append([7, 'coins', 0])
        self.cards.append([10, 'coins', 2])
        self.cards.append([11, 'coins', 3])
        self.cards.append([12, 'coins', 4])

        # Cups
        self.cards.append([1, 'cups', 11])
        self.cards.append([2, 'cups', 0])
        self.cards.append([3, 'cups', 10])
        self.cards.append([4, 'cups', 0])
        self.cards.append([5, 'cups', 0])
        self.cards.append([6, 'cups', 0])
        self.cards.append([7, 'cups', 0])
        self.cards.append([10, 'cups', 2])
        self.cards.append([11, 'cups', 3])
        self.cards.append([12, 'cups', 4])

        # Clubs
        self.cards.append([1, 'clubs', 11])
        self.cards.append([2, 'clubs', 0])
        self.cards.append([3, 'clubs', 10])
        self.cards.append([4, 'clubs', 0])
        self.cards.append([5, 'clubs', 0])
        self.cards.append([6, 'clubs', 0])
        self.cards.append([7, 'clubs', 0])
        self.cards.append([10, 'clubs', 2])
        self.cards.append([11, 'clubs', 3])
        self.cards.append([12, 'clubs', 4])


        #Shuffle deck
        for i in range(0, random.randint(0,100)):
            random.shuffle(self.cards)

        #Deal Player A Hand
        for i in range(0,3):
            index = random.randint(0,len(self.cards)-1)
            self.playerAHand.append(self.cards.pop(index))

        #Deal Player B Hand
        for j in range(0,3):
            index = random.randint(0, len(self.cards)-1)
            self.playerBHand.append(self.cards.pop(index))

        #Select trump card
        trumpIndex = random.randint(0, len(self.cards)-1)
        self.trump = self.cards.pop(trumpIndex);

        moves = self.playerAHand
        self.cardsNotPlayed = self.cards.copy()
        self.cardsNotPlayed.extend(self.playerBHand)

        
        self.initial = GameState(to_move='A', utility=0, board={'playerAHand':self.playerAHand, 'playerAPlayedCard':None, 'playerBPlayedCard':None,'cardsPlayed':[], 'cardsNotPlayed': self.cardsNotPlayed,'trumpCard':self.trump,'playerAPoints':0, 'playerBPoints':0, 'leadingPlayer':None}, moves=moves)
        
        window = tk.Tk();
        window.withdraw()

        
        
    def setSimulationCards(self, state):
        self.playerAHand = copy.deepcopy(state.board['playerAHand'])
        self.cards = copy.deepcopy(state.board['cardsNotPlayed'])
        self.trump = copy.deepcopy(state.board['trumpCard'])

        # Deal Player B Hand
        for j in range(0, 3):
            index = random.randint(0, len(self.cards)-1)
            self.playerBHand.append(self.cards.pop(index))

        
        moves = self.playerAHand
        self.cardsNotPlayed = copy.deepcopy(self.cards)
        self.cardsNotPlayed.extend(copy.deepcopy(self.playerBHand))
        self.initial = GameState(to_move=state.to_move, utility=state.utility, board=state.board, moves=state.moves)

    def startGame(self):
        self.play_game()


    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return state.moves


    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        board = state.board.copy()

        if(state.board['playerBPlayedCard'] is None and state.to_move == 'A'):
            board['leadingPlayer'] = 'A'
            board['playerAPlayedCard'] = move
            return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)
        elif(state.board['playerAPlayedCard'] is None and state.to_move == 'B'):
            board['leadingPlayer'] = 'B'
            board['playerBPlayedCard'] = move
            return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)
        else:

            if(state.to_move == 'A'):
                board['playerAPlayedCard'] = move
            elif(state.to_move == 'B'):
                board['playerBPlayedCard'] = move

            playerAPlayedCard = board['playerAPlayedCard']
            playerBPlayedCard = board['playerBPlayedCard']
            trumpCard = board['trumpCard']

            """for i in range(0, len(self.playerAHand)-1):
                if(self.playerAHand[i] == playerAPlayedCard):
                    del self.playerAHand[i]

            for i in range(0, len(self.playerBHand) - 1):
                if (self.playerBHand[i] == playerBPlayedCard):
                    del self.playerBHand[i]"""

            #self.playerAHand.remove(playerAPlayedCard)
            #self.playerBHand.remove(playerBPlayedCard)
            self.playerAHand = [x for x in self.playerAHand if x != playerAPlayedCard]
            self.playerBHand = [x for x in self.playerBHand if x != playerBPlayedCard]



            board['cardsNotPlayed'] = [x for x in board['cardsNotPlayed'] if x != playerBPlayedCard]
            board['cardsPlayed'].append(playerAPlayedCard)
            board['cardsPlayed'].append(playerBPlayedCard)

            board['playerAPlayedCard'] = None
            board['playerBPlayedCard'] = None

            if (playerAPlayedCard[1] == playerBPlayedCard[1]):  # Same card type
                if (playerAPlayedCard[2] > playerBPlayedCard[2]):  # A won the hand
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(trumpCard)
                        else:
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                    self.playerAPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                    board['leadingPlayer'] = ''
                    return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)

                elif (playerBPlayedCard[2] > playerAPlayedCard[2]):  # B won the hand
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(trumpCard)
                        else:
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                    self.playerBPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                    board['leadingPlayer'] = ''
                    return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)

                elif (playerAPlayedCard[0] > playerBPlayedCard[0]):  # Same value, higher number wins
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(trumpCard)
                        else:
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                    self.playerAPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                    board['leadingPlayer'] = ''
                    return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)

                elif (playerBPlayedCard[0] > playerAPlayedCard[0]):  # Higher number wins
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(trumpCard)
                        else:
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                self.playerBPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                board['leadingPlayer'] = ''
                return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)

            elif (playerAPlayedCard[1] == trumpCard[1]):  # A won the hand
                if (len(self.cards) != 0):
                    if (len(self.cards) == 1):
                        self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                        # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                        self.playerBHand.append(trumpCard)
                    else:
                        self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                        # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                        self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                self.playerAPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                board['leadingPlayer'] = ''
                return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)

            elif (playerBPlayedCard[1] == trumpCard[1]):  # B won the hand
                if (len(self.cards) != 0):
                    if (len(self.cards) == 1):
                        self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                        self.playerAHand.append(trumpCard)
                    else:
                        self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                        self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                        # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                self.playerBPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                board['leadingPlayer'] = ''
                return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)

            else:  # Leading player wins the hand
                if (board['leadingPlayer'] == 'A'):
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(trumpCard)
                        else:
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                    self.playerAPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                    board['leadingPlayer'] = ''
                    return GameState(to_move='A', utility=self.playerAPoints, board=board,
                                     moves=self.playerAHand)
                elif (board['leadingPlayer'] == 'B'):
                    if (len(self.cards) != 0):
                        if (len(self.cards) == 1):
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(trumpCard)
                        else:
                            self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                            self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                            # board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                    board['leadingPlayer'] = ''
                    self.playerBPoints += playerAPlayedCard[2] + playerBPlayedCard[2]
                    return GameState(to_move='B', utility=self.playerAPoints, board=board,
                                     moves=self.playerBHand)


    def utility(self, state, player):
        """Return the value of this final state to player."""
        return self.playerAPoints

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return len(self.cards) == 0 and len(self.playerAHand) == 0 and len(self.playerBHand) == 0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        #print(state)

        print('Player A\'s points: ' + str(self.playerAPoints))
        print('Player B\'s points: ' + str(self.playerBPoints))
        print('Trump Card: [' + str(state.board['trumpCard'][0]) + ' of ' + state.board['trumpCard'][1].upper() + "]")
        print('Cards left in deck: ' + str(len(self.cards)))
        
        numberOfCards = len(self.playerAHand)
        for i in range(0, numberOfCards):
            card = self.playerAHand[i]
            if(i == 0):
                movesStr = str(card[0]) + ' of ' + card[1].upper()
            else:
                movesStr += ']   [' + str(card[0]) + ' of ' + card[1].upper()
        print('Player A Hand: [' + movesStr + ']')

        if(state.board['playerAPlayedCard'] is not None):
            print('\n\n\t\t\t\tPlayer A played: [' + str(state.board['playerAPlayedCard'][0]) + ' of ' + state.board['playerAPlayedCard'][1].upper() + "]")
        else:
            print('\n\n\t\t\t\tPlayer A has not played')

        print('\nTurn: ' + state.to_move)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self):
        """Play against the AI."""
        state = self.initial

        while True:
            if(state.to_move == 'A'):
                move = alphabeta_player(game, state)

                if(state.board['leadingPlayer'] == 'B'):
                    print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    print('\n\n\t\t\t\tPlayer A played: [' + str(move[0]) + ' of ' + move[1].upper() + "]")
                    print('\n\n\t\t\t\tPlayer B played: [' + str(state.board['playerBPlayedCard'][0]) + ' of ' + state.board['playerBPlayedCard'][1].upper() + "]")
                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')


                state = self.result(state, move)

                if self.terminal_test(state):
                    #self.display(state)
                    resultStr = 'Player A\'s points: ' + str(self.playerAPoints) + '\nPlayer B\'s points: ' + str(self.playerBPoints)
                    messagebox.showinfo("Result", resultStr)
                    

                    return self.utility(state, self.to_move(self.initial))

            else:
                move = query_player(game, state)

                if (state.board['leadingPlayer'] == 'A'):
                    print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    if(state.board['playerAPlayedCard'] is not None):
                        print('\n\n\t\t\t\tPlayer A played: [' + str(state.board['playerAPlayedCard'][0]) + ' of ' + state.board['playerAPlayedCard'][1].upper() + "]")
                    else:
                        print('\n\n\t\t\t\tPlayer A has not played')

                    print('\n\n\t\t\t\tPlayer B played: [' + str(move[0]) + ' of ' + move[1].upper() + "]")
                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

                state = self.result(state, move)
                if self.terminal_test(state):
                    # self.display(state)
                    resultStr = 'Player A\'s points: ' + str(self.playerAPoints) + '\nPlayer B\'s points: ' + str(self.playerBPoints)
                    messagebox.showinfo("Result", resultStr)
                    return self.utility(state, self.to_move(self.initial))



game = Briscas()
game.initGame()
game.startGame()


