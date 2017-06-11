"""Games, or Adversarial Search (Chapter 5)"""

from collections import namedtuple
import random

from utils import argmax
from canvas import Canvas

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


def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        #MonteCarlo simulation
            v = min_value(game.result(state, a), best_score, beta)
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
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
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
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move_string = input('Your move? [0 for first card, 1 for second card, 2 for third card]: ')

    try:
        index = int(move_string)
    except ValueError:
        print('RIP')

    move = game.actions(state)[index]

    return move;



def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)


# ______________________________________________________________________________
# Some Sample Games


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
class Card:
    def __init__(self, number, type, value):
        self.number = number
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.number) + ' of ' + self.type

    def __repr__(self):
        return str(self.number) + ' of ' + self.type






class Briscas(Game):

    def __init__(self):
        """Set initial state (player turn, vida, cards in hand)"""
        # Cards definition / instantiation
        self.cards = []
        self.playerAHand = []
        self.playerBHand = []
        self.playerAPoints = 0
        self.playerBPoints = 0
        self.leadingPlayer = ''



        # Swords
        self.cards.append(Card(1, 'swords', 11))
        self.cards.append(Card(2, 'swords', 0))
        self.cards.append(Card(3, 'swords', 10))
        self.cards.append(Card(4, 'swords', 0))
        self.cards.append(Card(5, 'swords', 0))
        self.cards.append(Card(6, 'swords', 0))
        self.cards.append(Card(7, 'swords', 0))
        self.cards.append(Card(10, 'swords', 2))
        self.cards.append(Card(11, 'swords', 3))
        self.cards.append(Card(12, 'swords', 4))

        # Coins
        self.cards.append(Card(1, 'coins', 11))
        self.cards.append(Card(2, 'coins', 0))
        self.cards.append(Card(3, 'coins', 10))
        self.cards.append(Card(4, 'coins', 0))
        self.cards.append(Card(5, 'coins', 0))
        self.cards.append(Card(6, 'coins', 0))
        self.cards.append(Card(7, 'coins', 0))
        self.cards.append(Card(10, 'coins', 2))
        self.cards.append(Card(11, 'coins', 3))
        self.cards.append(Card(12, 'coins', 4))

        # Cups
        self.cards.append(Card(1, 'cups', 11))
        self.cards.append(Card(2, 'cups', 0))
        self.cards.append(Card(3, 'cups', 10))
        self.cards.append(Card(4, 'cups', 0))
        self.cards.append(Card(5, 'cups', 0))
        self.cards.append(Card(6, 'cups', 0))
        self.cards.append(Card(7, 'cups', 0))
        self.cards.append(Card(10, 'cups', 2))
        self.cards.append(Card(11, 'cups', 3))
        self.cards.append(Card(12, 'cups', 4))

        # Clubs
        self.cards.append(Card(1, 'clubs', 11))
        self.cards.append(Card(2, 'clubs', 0))
        self.cards.append(Card(3, 'clubs', 10))
        self.cards.append(Card(4, 'clubs', 0))
        self.cards.append(Card(5, 'clubs', 0))
        self.cards.append(Card(6, 'clubs', 0))
        self.cards.append(Card(7, 'clubs', 0))
        self.cards.append(Card(10, 'clubs', 2))
        self.cards.append(Card(11, 'clubs', 3))
        self.cards.append(Card(12, 'clubs', 4))


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
        self.cardsNotPlayed.extend(self.playerBHand.copy())

        self.initial = GameState(to_move='A', utility=0, board={'playerAHand':self.playerAHand, 'playerAPlayedCard':[], 'playerBPlayedCard':[],'cardsPlayed':[], 'cardsNotPlayed': self.cardsNotPlayed,'trumpCard':self.trump,'playerAPoints':0, 'playerBPoints':0}, moves=moves)
        self.play_game(query_player, query_player)

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return state.moves


    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        board = state.board.copy()


        if(state.board['playerBPlayedCard']==[] and state.to_move == 'A'):
            self.leadingPlayer = 'A'
            board['playerAPlayedCard'] = move
            return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)
        elif(state.board['playerAPlayedCard']==[] and state.to_move == 'B'):
            self.leadingPlayer = 'B'
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


            board['playerAPlayedCard'] = []
            board['playerBPlayedCard'] = []
            self.playerAHand.remove(playerAPlayedCard)
            self.playerBHand.remove(playerBPlayedCard)
            board['cardsPlayed'].append(playerAPlayedCard)
            board['cardsPlayed'].append(playerBPlayedCard)

            board['cardsNotPlayed'].remove(playerBPlayedCard)




            if(playerAPlayedCard.type != trumpCard.type and playerBPlayedCard.type != trumpCard.type):
                if(playerAPlayedCard.type == playerBPlayedCard.type):
                    if(playerAPlayedCard.value > playerBPlayedCard.value): #A won the hand
                        if(len(self.cards) != 0):
                            if(len(self.cards) == 1):
                                self.playerAHand.append(self.cards.pop(len(self.cards)-1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(trumpCard)
                            else:
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                        self.playerAPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)

                    else:   #B won the hand
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(trumpCard)
                            else:
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                        self.playerBPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)

                else:
                    if(self.leadingPlayer == 'A'):
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(trumpCard)
                            else:
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                        self.playerAPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        self.leadingPlayer = ''
                        return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)
                    elif(self.leadingPlayer == 'B'):
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(trumpCard)
                            else:
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                        self.leadingPlayer = ''
                        self.playerBPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)
            else:
                if(playerAPlayedCard.type == trumpCard.type and playerBPlayedCard.type == trumpCard.type):
                    if (playerAPlayedCard.value > playerBPlayedCard.value):  # A won the hand
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(trumpCard)
                            else:
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                        self.playerAPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)

                    else:  # B won the hand
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(trumpCard)
                            else:
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                        self.playerBPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)

                else:
                    if(playerAPlayedCard.type == trumpCard.type): #A won the hand
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(trumpCard)
                            else:
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))

                        self.playerAPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='A', utility=self.playerAPoints, board=board, moves=self.playerAHand)
                    else:   #B won the hand
                        if (len(self.cards) != 0):
                            if (len(self.cards) == 1):
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(trumpCard)
                            else:
                                self.playerBHand.append(self.cards.pop(len(self.cards) - 1))
                                self.playerAHand.append(self.cards.pop(len(self.cards) - 1))
                                board['cardsNotPlayed'].remove(self.playerAHand[len(self.playerAHand)-1])

                        self.playerBPoints += playerAPlayedCard.value + playerBPlayedCard.value
                        return GameState(to_move='B', utility=self.playerAPoints, board=board, moves=self.playerBHand)


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
        print('Trump Card: ' + str(state.board['trumpCard']))
        print('Cards left in deck: ' + str(len(self.cards)))

        print('\nTurn: ' + state.to_move)

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


game = Briscas()


