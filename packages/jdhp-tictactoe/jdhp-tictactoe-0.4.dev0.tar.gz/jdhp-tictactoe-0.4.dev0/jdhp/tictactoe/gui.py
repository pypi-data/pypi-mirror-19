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

# See: http://effbot.org/tkinterbook/canvas.htm

"""
TODO...
"""

__all__ = ['TkGUI']

from jdhp.tictactoe.game import Game
from jdhp.tictactoe.player.greedy import GreedyPlayer
from jdhp.tictactoe.player.human import HumanPlayer
from jdhp.tictactoe.player.random import RandomPlayer

import random
import tkinter as tk

SQUARE_NUM = 3    # squares per side

class TkGUI:
    """
    TODO...
    """

    def __init__(self):
        """
        TODO...
        """

        # Game attributes #############

        self.game = Game()
        self.player_list = None
        self.current_player_index = None
        self.current_state = None

        # GUI parameters ##############

        # TODO...
        self.square_size = 128 # pixels
        self.symbol_offset = 20
        self.symbol_line_width = 12
        self.grid_line_width = 8

        self.square_color = "white"
        self.player1_over_square_color = "red"
        self.player2_over_square_color = "green"
        self.over_wrong_square_color = "white"   # "gray"

        self.player1_symbol_color = "red"
        self.player2_symbol_color = "green"

        # Make the main window ########

        self.root = tk.Tk()                # TODO
        self.root.resizable(False, False)  # <- Lock the size of the window

        # Make widgets ################

        self.available_player_type_list = ["Human",
                                           "Computer (easy)",
                                           "Computer (very easy)"]

        # Player1 option menu
        player1_label = tk.Label(self.root, text="Player 1 (X):")
        player1_label.grid(row=0, column=0, padx=8, sticky="w")

        self._player1_var = tk.StringVar()
        self._player1_var.set(self.available_player_type_list[0])
        self.player1_optionmenu = tk.OptionMenu(self.root,
                                           self._player1_var,
                                           *self.available_player_type_list)
                                           #command=self.set_player1)
        self.player1_optionmenu.config(width=24)
        self.player1_optionmenu.grid(row=0, column=1, sticky="we")

        # Player2 option menu
        player2_label = tk.Label(self.root, text="Player 2 (O):")
        player2_label.grid(row=1, column=0, padx=8, sticky="w")

        self._player2_var = tk.StringVar()
        self._player2_var.set(self.available_player_type_list[0])
        self.player2_optionmenu = tk.OptionMenu(self.root,
                                           self._player2_var,
                                           *self.available_player_type_list)
                                           #command=self.set_player2)
        self.player2_optionmenu.config(width=24)
        self.player2_optionmenu.grid(row=1, column=1, sticky="we")

        # Canvas
        self.canvas = tk.Canvas(self.root,
                                width=SQUARE_NUM*self.square_size,
                                height=SQUARE_NUM*self.square_size)
        self.canvas.grid(row=2, column=0, columnspan=2, sticky="nswe")

        self.lock_canvas()

        self.canvas.tag_bind("square",                      # a tag string or an item id
                             "<Button-1>",                  # the event descriptor
                             self.click_on_canvas_callback, # the callback function
                             add="+")                       # "+" to add this binding to the previous one(s) (i.e. keep the previous binding(s)) or None to replace it or them

        self.canvas.create_text((self.square_size * 1.5, self.square_size * 1.5),
                                text="Define players then press start",
                                font="Sans 12 bold",
                                fill="gray",
                                anchor="center")  # n, ne, e, se, s, sw, w, nw, or center

        # Status label
        self.status_label = tk.Label(self.root,
                                     font="Sans 12 bold",
                                     foreground="#000000",
                                     text="")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="we")

        # Start / Quit / Restart button
        self.button = tk.Button(self.root, text="Start", command=self.start)
        self.button.grid(row=4, column=0, columnspan=2, sticky="we")

    ###################################

    def run(self):
        """
        TODO...
        """
        # Tk event loop
        # TODO ???
        self.root.mainloop()

    ###################################

    def start(self):
        """
        TODO...
        """
        self.lock_player_option_menus()

        self.status_label["text"] = ""
        #self.status_label["font"] = "Sans 12 bold"
        #self.status_label["foreground"] = "#000000"

        # Change button's label and callback funtion
        self.button["text"] = "Quit"
        self.button["command"] = self.stop

        # Init game state
        self.player_list = [None, None]                         # TODO

        if self.get_player1_type() == "Human":                  # TODO
            self.player_list[0] = HumanPlayer("X")
        elif self.get_player1_type() == "Computer (easy)":      # TODO
            self.player_list[0] = GreedyPlayer("X")
        elif self.get_player1_type() == "Computer (very easy)": # TODO
            self.player_list[0] = RandomPlayer("X")
        else:
            raise Exception("Internal error")

        if self.get_player2_type() == "Human":                  # TODO
            self.player_list[1] = HumanPlayer("O")
        elif self.get_player2_type() == "Computer (easy)":      # TODO
            self.player_list[1] = GreedyPlayer("O")
        elif self.get_player2_type() == "Computer (very easy)": # TODO
            self.player_list[1] = RandomPlayer("O")
        else:
            raise Exception("Internal error")

        self.current_player_index = random.randint(0, 1) # TODO
        self.current_state = self.game.getInitialState()

        # Display the game grid
        self.draw_current_state()

        # Call the play loop
        self.play_loop()

    def stop(self):
        """
        TODO...
        """
        self.lock_canvas()
        self.unlock_player_option_menus()

        # Change button's label and callback funtion
        self.button["text"] = "Start"
        self.button["command"] = self.start

        # Display score
        if self.game.isFinal(self.current_state, self.player_list):
            if self.game.hasWon(self.player_list[0], self.current_state):
                self.status_label["text"] = "Player1 has won!"
                #self.status_label["font"] = "Sans 12 bold"
                #self.status_label["foreground"] = "#000000"
            elif self.game.hasWon(self.player_list[1], self.current_state):
                self.status_label["text"] = "Player2 has won!"
                #self.status_label["font"] = "Sans 12 bold"
                #self.status_label["foreground"] = "#000000"
            else:
                self.status_label["text"] = "Draw!"
                #self.status_label["font"] = "Sans 12 bold"
                #self.status_label["foreground"] = "#000000"

    def lock_player_option_menus(self):
        """
        Lock the player selection menu so that the selection cannot change.
        """
        self.player1_optionmenu["state"] = "disabled"
        self.player2_optionmenu["state"] = "disabled"

    def unlock_player_option_menus(self):
        """
        Unlock the player selection menu so that users can change the
        selection.
        """
        self.player1_optionmenu["state"] = "normal"
        self.player2_optionmenu["state"] = "normal"

    def lock_canvas(self):
        """
        Lock the canvas so that users cannot play.
        """
        self.canvas["state"] = "disabled"

    def unlock_canvas(self):
        """
        Unlock the canvas so that users can play.
        """
        self.canvas["state"] = "normal"

    ###################################

    def get_player1_type(self):
        """
        TODO...
        """
        return self._player1_var.get()

    def get_player2_type(self):
        """
        TODO...
        """
        return self._player2_var.get()

    ###################################

    def play_loop(self):
        """
        TODO...
        """
        current_player = self.player_list[self.current_player_index]
        is_final = self.game.isFinal(self.current_state, self.player_list)

        # While computer plays
        while (not isinstance(current_player, HumanPlayer)) and (not is_final):
            action = self.player_list[self.current_player_index].play(self.game, self.current_state)  # TODO: execute this function in a separate thread to avoid Tk lock
            self.play(action)
            current_player = self.player_list[self.current_player_index]       # TODO
            is_final = self.game.isFinal(self.current_state, self.player_list) # TODO

        # Let (human) user play
        if not is_final:               # TODO
            self.draw_current_state()  # TODO (to update the "over square color"...)
            self.status_label["text"] = "{} Turn".format(current_player.symbol)
            self.unlock_canvas()


    def play(self, action):
        """
        TODO...
        """
        current_player = self.player_list[self.current_player_index]

        self.current_state = self.game.nextState(self.current_state,
                                                 action,
                                                 current_player)

        self.draw_current_state()

        if self.game.isFinal(self.current_state, self.player_list):
            self.stop()
        else:
            self.current_player_index = (self.current_player_index + 1) % 2

    ###################################

    def click_on_canvas_callback(self, event):                 # event is a tkinter.Event object
        """
        TODO...
        """
        id_tuple = self.canvas.find_withtag("current")  # get the item which is under the mouse cursor

        if len(id_tuple) > 0:
            item_id = id_tuple[0]
            #print(self.canvas.gettags(item_id))
            item_tag1, item_tag2, item_tag3 = self.canvas.gettags(item_id)
            #print("square {} (item #{})".format(item_tag2, item_id))

            action = int(item_tag2)

            if self.game.isValidAction(self.current_state, action):
                self.lock_canvas()
                self.play(action)  # TODO
                self.play_loop()   # TODO
        else:
            raise Exception("Unexpected error")

    def draw_current_state(self):
        """
        TODO...
        """
        # Clear the canvas (remove all shapes)
        self.canvas.delete(tk.ALL)

        for row_index in range(SQUARE_NUM):
            # Make squares
            for col_index in range(SQUARE_NUM):
                square_index = row_index * 3 + col_index
                color = self.square_color
                tags = ("square", "{}".format(square_index))

                if self.current_state is not None:
                    if self.current_state[square_index] != " ":
                        active_fill_color = self.over_wrong_square_color
                    elif self.current_player_index == 0:
                        active_fill_color = self.player1_over_square_color
                    elif self.current_player_index == 1:
                        active_fill_color = self.player2_over_square_color
                    else:
                        raise Exception("Internal error")

                self.canvas.create_rectangle(self.square_size * col_index,       # x1
                                             self.square_size * (2 - row_index), # y1
                                             self.square_size * (col_index + 1), # x2
                                             self.square_size * (3 - row_index), # y2
                                             tag=tags,
                                             fill=color,
                                             activefill=active_fill_color,
                                             width=0)

                if self.current_state is not None:
                    
                    off = self.symbol_offset

                    if self.current_state[square_index] == "X":
                        line_coordinates = (self.square_size * col_index + off,       # x1
                                            self.square_size * (2 - row_index) + off, # y1
                                            self.square_size * (col_index + 1) - off, # x2
                                            self.square_size * (3 - row_index) - off) # y2

                        self.canvas.create_line(line_coordinates,
                                                fill=self.player1_symbol_color,
                                                width=self.symbol_line_width)

                        line_coordinates = (self.square_size * col_index + off,       # x1
                                            self.square_size * (3 - row_index) - off, # y1
                                            self.square_size * (col_index + 1) - off, # x2
                                            self.square_size * (2 - row_index) + off) # y2

                        self.canvas.create_line(line_coordinates,
                                                fill=self.player1_symbol_color,
                                                width=self.symbol_line_width)

                    elif self.current_state[square_index] == "O":
                        line_coordinates = (self.square_size * col_index + off,       # x1
                                            self.square_size * (2 - row_index) + off, # y1
                                            self.square_size * (col_index + 1) - off, # x2
                                            self.square_size * (3 - row_index) - off) # y2

                        self.canvas.create_oval(line_coordinates,
                                                outline=self.player2_symbol_color,
                                                width=self.symbol_line_width)

        # Draw vertical lines
        for col_index in range(1, SQUARE_NUM):
            line_coordinates = (self.square_size * col_index,  # x1
                                0,                        # y1
                                self.square_size * col_index,  # x2
                                self.square_size * SQUARE_NUM) # y2

            self.canvas.create_line(line_coordinates,
                                    fill="black",
                                    width=self.grid_line_width)

        # Draw horizontal lines
        for row_index in range(1, SQUARE_NUM):
            line_coordinates = (0,                        # x1
                                self.square_size * row_index,  # y1
                                self.square_size * SQUARE_NUM, # x2
                                self.square_size * row_index)  # y2

            self.canvas.create_line(line_coordinates,
                                    fill="black",
                                    width=self.grid_line_width)


def main():
    """
    TODO...
    """
    gui = TkGUI()

    # Launch the main loop
    gui.run()


if __name__ == '__main__':
    main()

