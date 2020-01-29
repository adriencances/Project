from tkinter import *
import os

# path depending on computeur files : HAVE TO BE CHANGED
os.chdir("D:/Documents/Ecole/2A/Tdlog/Interface/Interface")

from computations import prob_win

class Card:
    """
    Card has a value and belongs to a window and interface
    Fonctions button display the card on a button with specific a command
    """

    def __init__ (self, val, window, interface, row=0, column=0):
        self.set_val(val)
        self.row = row
        self.column = column
        self.window = window
        self.interface = interface

    def print_val (self):
        """
        return the int value of the card and close the current window
        it is used by the card selector
        """
        global selected_val
        selected_val = self.val
        self.window.destroy()

    def set_val (self, val):
        """
        change the value and the picture path of the card
        """
        if(val in range(54)):
            self.val = val
            self.path = 'Images/%s.png' %(val)
        else:
            print("Value out of range")

    def button_val (self):
        """
        create a button linked with the command print_val
        it is used on the card selector
        """
        self.im = PhotoImage(master=self.window, file=self.path)
        self.bout = Button(self.window, image=self.im, command=self.print_val, bd='5')
        self.bout.grid(row=self.row, column=self.column, ipadx=7, ipady=7)

    def button_card (self, id_button):
        """
        create a button linked with the command set_card of the 9 different position cards
        it is used on the main interface
        """
        self.im = PhotoImage(master=self.window, file=self.path)
        if (self.val==53):
            self.bout = Button(self.window, image=self.im, bd='5')
        else:
            self.bout = Button(self.window, image=self.im, command = lambda : self.interface.set_card(id_button), bd='5')
        if id_button != 7:
            self.bout.grid(row=self.row, column=self.column, ipadx=7, ipady=7)
        else :
            self.bout.grid(row=self.row, column=self.column, padx=20, ipadx=7, ipady=7)

class Interface :
    """
    Interface in which the user can select cards and compute the winning probabilities
    there are nine cards : 2 player cards, 2 opponent cards, 3 flop cards, 1 turn card and 1 river card
    """

    def __init__(self, window, int_cards=[52,52,52,52,52,52,52,52,52]):
        self.int_cards = int_cards
        self.player_cards = [Card(int_cards[0], window, self, 4, 0), Card(int_cards[1], window, self, 4, 1)]
        self.opponent_cards = [Card(int_cards[2], window, self, 0, 0), Card(int_cards[3], window, self, 0, 1)]
        self.flop = [Card(int_cards[4], window, self, 2, 0), Card(int_cards[5], window, self, 2, 1), Card(int_cards[6], window, self, 2, 2)]
        self.turn = [Card(int_cards[7], window, self, 2, 3)]
        self.river = [Card(int_cards[8], window, self, 2, 4)]
        self.cards = self.player_cards + self.opponent_cards + self.flop + self.turn + self.river
        self.window = window

    def display_buttons (self):
        """
        display the 9 card buttons, the button of calculation and different labels
        """
        Label(self.window, text="Opponent Cards").grid(row=1, column=0, sticky="n", columnspan=2, pady = 10)
        Label(self.window, text="Flop").grid(row=3, column=0, sticky="nsew", columnspan=3, rowspan=1, pady = 10)
        Label(self.window, text="Turn").grid(row=3, column=3, sticky="nsew", columnspan=1, rowspan=1)
        Label(self.window, text="River").grid(row=3, column=4, sticky="nsew", columnspan=1, rowspan=1)
        Label(self.window, text="Player Cards").grid(row=5, column=0, sticky="nsew", columnspan=2, pady = 10)
        if(self.condition_of_calculation()):
            Button(self.window, text='Compute \n winning probabilities', command=self.compute).grid(row=2, column=5, sticky="nsew",padx=20, ipadx=7, ipady=15)
        else:
            Button(self.window, text='Choose player cards \n and at least the 3 flop cards \n or the 2 opponent cards').grid(row=2, column=5, sticky="nsew",padx=20, ipadx=7, ipady=15)
        for i in range (9):
            self.cards[i].button_card(i)

    def condition_of_calculation(self):
        """
        return a boolean depending if the selection of cards enables calculation of probabilities
        """
        if(self.int_cards[0]<52 and self.int_cards[1]<52):
            if(self.int_cards[4]==52 or self.int_cards[5]==52 or self.int_cards[6]==52):
                if(self.int_cards[4]<52 or self.int_cards[5]<52 or self.int_cards[6]<52):
                    return False
            if(self.int_cards[2]==52 or self.int_cards[3]==52):
                if(self.int_cards[2]<52 or self.int_cards[3]<52):
                    return False
            if(self.int_cards[4]<51 and self.int_cards[5]<51 and self.int_cards[6]<51):
                return True
            if(self.int_cards[2]<51 and self.int_cards[3]<51):
                return True
        return False


    def set_card(self, id_button):
        """
        change the card of the main interface
        """
        self.window.destroy()
        global cards
        int_cards = self.int_cards
        int_cards[id_button] = choose_card(self.int_cards, self)
        open_interface(int_cards)

    def compute(self):
        """
        compute and display winning probabilities
        """
        proba_pla = int(round(prob_win(self.int_cards)*100, 0))
        proba_opp = int(round(100-proba_pla, 0))
        Label(self.window, text= str(proba_opp)+'%').grid(row=0, column=5, sticky="nsew",padx=20, ipadx=7, ipady=15)
        Label(self.window, text= str(proba_pla)+'%').grid(row=4, column=5, sticky="nsew",padx=20, ipadx=7, ipady=15)

def choose_card (selected_card, interface):
    """
    open a new window in which the user can choose a card
    return the value of the card
    """
    global selected_val
    selected_val = 52
    window = Tk()
    card_list = [Card(i*13+j, window, interface, i, j) for i in range(4) for j in range(13)]
    for i in range(52):
        if(i in selected_card):
            card_list[i].set_val(52)
        card_list[i].button_val()
    window.mainloop()
    return(selected_val)

def open_interface (int_cards=[12,25,52,52,15,41,32,10,18]):
    """
    create and display the main interface in which the user can
    choose the cards known and compute the winning probabilities
    """
    updated_cards = update_button(int_cards)
    window = Tk()
    Int = Interface(window, updated_cards)
    Int.display_buttons()
    window.mainloop()

def update_button (int_cards):
    """
    uptade integer value of cards between 53 and 52 depending on the possibility to change the value of this card
    """
    for k in range(2,9):
        if (int_cards[k]==53):
            int_cards[k]=52
    if(int_cards[0]>51 or int_cards[1]>51):
        for i in range (2,9):
            int_cards[i]=53
    elif (int_cards[4]>51 or int_cards[5]>51 or int_cards[6]>51):
        int_cards[7]=53
        int_cards[8]=53
    elif (int_cards[7]>51):
        int_cards[8]=53
    return int_cards


open_interface()













