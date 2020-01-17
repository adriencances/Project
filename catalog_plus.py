#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 01:21:12 2019

@author: Adrien CANCES
"""

import itertools as it


"""
Used for readable card representation.
Example: Queen of spade -> "12s"
"""

RANKS = [rank for rank in range(2, 15)]
SUITS = ["s", "h", "c", "d"]
CARDS_REPR = [str(rank) + suit for suit in SUITS for rank in RANKS]
CARDS_NUM = dict([(CARDS_REPR[i], i) for i in range(52)])


"""
Used for calculations.
"""

CARDS = list(range(52))
CARD_PAIRS = list(it.combinations(CARDS, 2))
FIVE_CARD_SETS = list(it.combinations(CARDS, 5))



#RIVERS_HOLE_CARDS = [(river, list(hole_cards)) for hole_cards in CARD_PAIRS
#                     for river in CARDS if not river in hole_cards]
#
#SEVEN_CHOOSE_FIVE = list(it.combinations(range(7), 5))
#
#
#CATEGORY_HIERARCHY = {"high card": 0,
#                      "pair": 1,
#                      "double pair": 2,
#                      "three of a kind": 3,
#                      "straight": 4,
#                      "flush": 5,
#                      "full house": 6,
#                      "four of a kind": 7,
#                      "straight flush": 8}
#
#POSSIBLE_STRAIGHTS = [(i + 4, i + 3, i + 2, i + 1, i) for i in range(2, 11)] + [(14, 5, 4, 3, 2)]
#
#HIGH_CARDS_VAL = [val for val in reversed(list(it.combinations(range(14, 1, -1), 5)))
#                  if not val in POSSIBLE_STRAIGHTS]
## 1277
#
#PAIRS_VAL = [(i, j, k, l) for i in range(2, 15)
#             for j,k,l in reversed(list(it.combinations(range(14, 1, -1), 3)))
#             if not i in [j, k, l]]
## 2860
#
#DOUBLE_PAIRS_VAL = [(i, j, k) for i,j in reversed(list(it.combinations(range(14, 1, -1), 2)))
#                    for k in range(2, 15) if not k in [i,j]]
## 858
#
#THREE_OF_A_KINDS_VAL = [(i, j, k) for i in range(2, 15)
#                       for j,k in reversed(list(it.combinations(range(14, 1, -1), 2)))
#                       if not i in [j, k]]
## 858
#
#STRAIGHTS_VAL = [(i,) for i in range(5, 15)]
## 10
#
#FLUSHES_VAL = HIGH_CARDS_VAL
## 1277
#
#FULL_HOUSES_VAL = [(i, j) for i in range(2, 15) for j in range(2, 15) if i != j]
## 156
#
#FOUR_OF_A_KINDS_VAL = FULL_HOUSES_VAL
## 156
#
#STRAIGHT_FLUSHES_VAL = STRAIGHTS_VAL
## 10
#
#KEY_VAL_LIST = (
#        [((0, HIGH_CARDS_VAL[i]), i) for i in range(len(HIGH_CARDS_VAL))] +
#        [((1, PAIRS_VAL[i]), 1277 + i) for i in range(len(PAIRS_VAL))] +
#        [((2, DOUBLE_PAIRS_VAL[i]), 4137 + i) for i in range(len(DOUBLE_PAIRS_VAL))] +
#        [((3, THREE_OF_A_KINDS_VAL[i]), 4995 + i) for i in range(len(THREE_OF_A_KINDS_VAL))] +
#        [((4, STRAIGHTS_VAL[i]), 5853 + i) for i in range(len(STRAIGHTS_VAL))] +
#        [((5, FLUSHES_VAL[i]), 5863 + i) for i in range(len(FLUSHES_VAL))] +
#        [((6, FULL_HOUSES_VAL[i]), 7140 + i) for i in range(len(FULL_HOUSES_VAL))] +
#        [((7, FOUR_OF_A_KINDS_VAL[i]), 7296+ i) for i in range(len(FOUR_OF_A_KINDS_VAL))] +
#        [((8, STRAIGHT_FLUSHES_VAL[i]), 7452 + i) for i in range(len(STRAIGHT_FLUSHES_VAL))]
#        )
#
#CAT_VALUES = dict(KEY_VAL_LIST)