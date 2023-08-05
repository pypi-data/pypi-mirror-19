# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
TODO...
"""

__all__ = ['Game']

import copy

class Game:
    """
    TODO...
    """

    def getInitialState(self):
        """
        TODO...
        """
        return [" "] * 9

    def getSetOfValidActions(self, state):
        """
        TODO...
        """
        # Get the list index of empty squares
        list_of_valid_actions = [index for index,symbol in enumerate(state) if symbol==" "]

        return list_of_valid_actions 

    def nextState(self, state, action, player):
        """
        TODO...
        """
        if not self.isValidState(state):
            raise Exception(ValueError("Wrong state value:", state))

        if not self.isValidAction(state, action):
            raise Exception(ValueError("Wrong state value:", state))

        next_state = copy.deepcopy(state)
        next_state[action] = player.symbol

        return next_state

    def isFinal(self, state, player_list):
        """
        TODO...
        """
        if not self.isValidState(state):
            raise Exception(ValueError("Wrong state value:", state))

        is_final = False

        # Check if there is at least one empty square
        if state.count(" ") == 0 or self.hasWon(player_list[0], state) or self.hasWon(player_list[1], state):
            is_final = True

        return is_final

    def hasWon(self, player, state):
        """
        TODO...
        """
        if not self.isValidState(state):
            raise Exception(ValueError("Wrong state value:", state))

        state_mask = [1 if value==player.symbol else 0 for value in state]

        has_won = False

        # Check lines
        if sum(state_mask[0:3])==3 or sum(state_mask[3:6])==3 or sum(state_mask[6:9])==3:
            has_won = True

        # Check columns
        elif sum(state_mask[0:9:3])==3 or sum(state_mask[1:9:3])==3 or sum(state_mask[2:9:3])==3:
            has_won = True

        # Check diagonals
        elif sum(state_mask[0:9:4])==3 or sum(state_mask[2:7:2])==3:
            has_won = True

        return has_won

    def isValidState(self, state):
        """
        TODO...
        """
        is_valid = True

        try:
            if len(state) == 9:
                for square_value in state:
                    if square_value not in [" ", "X", "O"]:
                        is_valid = False
                        break
            else:
                is_valid = False
        except:
            is_valid = False

        return is_valid

    def isValidAction(self, state, action):
        """
        TODO...
        """
        return (action in range(9)) and (state[action] == " ")


    def print_state(self, state):
        """
        TODO...
        Row count start from bottom like for chessboards.
        """
        print("  A B C")
        print(" +-+-+-+")
        print("3|{}|{}|{}|3".format(state[6], state[7], state[8]))
        print(" +-+-+-+")
        print("2|{}|{}|{}|2".format(state[3], state[4], state[5]))
        print(" +-+-+-+")
        print("1|{}|{}|{}|1".format(state[0], state[1], state[2]))
        print(" +-+-+-+")
        print("  A B C")

