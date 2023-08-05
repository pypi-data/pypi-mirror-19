#!/usr/bin/env python3
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

__all__ = ['run']

from jdhp.tictactoe.game import Game
from jdhp.tictactoe.player.random import RandomPlayer
from jdhp.tictactoe.player.human import HumanPlayer

import random

def run(quiet=False):
    """
    TODO...
    """
    game = Game()

    player_list = [HumanPlayer("X"),            # TODO
                   RandomPlayer("O")]           # TODO
    current_player_index = random.randint(0, 1) # TODO
    current_state = game.getInitialState()

    while not game.isFinal(current_state, player_list):
        current_player = player_list[current_player_index]
        action = current_player.play(game, current_state)
        current_state = game.nextState(current_state, action, current_player)
        current_player_index = (current_player_index + 1) % 2

    if not quiet:
        game.print_state(current_state)

        if game.hasWon(player_list[0], current_state):
            print("Player1 has won!")
        elif game.hasWon(player_list[1], current_state):
            print("Player2 has won!")
        else:
            print("Draw...")

if __name__ == '__main__':
    run()

