
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:46:45 2019

@authors: Adrien CANCES and Florentin POUCIN
"""

"""
rank(card) = card%13
suit(card) = card//13
"""

import itertools as it
import random as rd\

from catalog_plus import CARDS_REPR, CARDS_NUM, CARDS, CARD_PAIRS, FIVE_CARD_SETS



def numerical_cards(str_cards):
    """
    Converts a set of cards from string encoding to numerical encoding.
    Example : "13s 4c 5d" -> [11, 28, 42]
    """
    return [CARDS_NUM[str_card] for str_card in str_cards.split()]


def string_cards(num_cards):
    """
    Converts a set of cards from numerical encoding to string encoding.
    Example : [11, 28, 42] -> "13s 4c 5d"
    """
    return " ".join([CARDS_REPR[num_card] for num_card in num_cards])


def first_sublist_index(pattern, lst):
    """
    Returns the minimal index at which the pattern can be found in the list if
    the pattern is in the list, -1 otherwise.
    """
    for index in range(len(lst)):
        if lst[index] == pattern[0] and lst[index:index + len(pattern)] == pattern:
            return index
    return -1


def is_in_list(pattern, lst):
    """
    Returns True if and only if the pattern is in the list
    """
    for index in range(len(lst)):
        if lst[index] == pattern[0] and lst[index:index + len(pattern)] == pattern:
            return True
    return False


def decr_indices(elt, lst):
    """
    Returns the list of indices at which the element can be found in the list,
    sorted by decreasing order.
    """
    return [i for i in range(len(lst) - 1, - 1, -1) if lst[i] == elt]


def histograms(hand):
    """
    Returns the rank histogram and the suit histogram of a hand
    (a set of five cards).
    Example : [12, 45, 16, 3, 5] -> ([0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 1], [3, 1, 0, 1])
    """
    ranks = [card%13 for card in hand]
    suits = [card//13 for card in hand]
    histogram_ranks = [ranks.count(rk) for rk in range(13)]
    histogram_suits = [suits.count(st) for st in range(4)]
    return histogram_ranks, histogram_suits


def category(hist_ranks, hist_suits):
    """
    Returns an integer encoding the hand category the given pair of histograms
    belongs to. Below is the list of possible types.
    - high card: 0
    - pair: 1
    - double pair: 2
    - three of a kind: 3
    - straight: 4
    - flush: 5
    - full house: 6
    - four of a kind: 7
    - straight flush: 8
    """
    four_kind = 4 in hist_ranks
    if four_kind:
        return 7 # "four of a kind"
    three_kind = 3 in hist_ranks
    pair = 2 in hist_ranks
    if three_kind:
        if pair:
            return 6 # "full house"
        return 3 # "three of a kind"
    two_pairs = (hist_ranks.count(2) == 2)
    if two_pairs:
        return 2 # "double pair"
    if pair:
        return 1 # "pair"
    flush = 5 in hist_suits
    straight = is_in_list([1, 1, 1, 1, 1], hist_ranks)
    if hist_ranks == [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]: # if the straight starts by an Ace
        straight = True
    if flush:
        if straight:
            return 8 # "straight flush"
        return 5 # "flush"
    if straight:
        return 4 # "straight"
    return 0 # "high card"


def category_and_features(hand):
    """
    Returns the category and the features of the given hand.
    The features are used to compare two hands of the same category.
    They are the minimum amount of information necessary to compare two hands
    of a given category.
    """
    hist_ranks, hist_suits = histograms(hand)
    cat = category(hist_ranks, hist_suits)
    feat = tuple([rk + 2 for nb in [4, 3, 2, 1] for rk in decr_indices(nb, hist_ranks)])
    if cat in [4, 8]: # ["straight", "straight flush"]
        if 2 in feat and 14 in feat:
            feat = (5,)
        else:
            feat = (feat[0],)
    return cat, feat


def best_cat_feat(seven_cards):
    """
    Returns the category and the features of the best hand that can be found
    in the given set of seven cards.
    """
    cat_feats = [category_and_features(hand) for hand
                in list(it.combinations(seven_cards, 5))]
    return max(cat_feats)




# TEMPORARY
def summary(results):
    print("Mean: ", sum(results)/len(results))
    print("Min: ", min(results))
    print("Max: ", max(results))




hc = numerical_cards("14s 7d")
ft = numerical_cards("2d 4h 5d 8s")
ftr = numerical_cards("2d 4h 5d 8s 6s")
hc_1 = numerical_cards("13s 3d")
hc_2 = numerical_cards("11s 12d")
flp = numerical_cards("4s 5d 9s")




"""
OPPONENT CARDS NOT KNOWN
"""


def prob_win_river(hole_cards, flop_turn_river):
    """
    Probability that player 1 wins knowing his cards and the five cards on the table.
    """
    nb_total = 45*22
    nb_win_1 = 0
    known_cards = hole_cards + flop_turn_river
    cat_val_1 = best_cat_feat(known_cards)
    for card_1, card_2 in CARD_PAIRS:
        if not card_1 in known_cards and not card_2 in known_cards:
            cat_val_2 = best_cat_feat([card_1, card_2] + flop_turn_river)
            if cat_val_1 > cat_val_2:
                nb_win_1 += 1
            elif cat_val_1 == cat_val_2:
                nb_win_1 += 0.5
    return nb_win_1/nb_total

#print(prob_win_river(hc_2, ftr))


def prob_win_turn(hole_cards, flop_turn):
    """
    Probability that player 1 wins knowing his cards, the flop, and the turn.
    We do not use it given its quite long execution time (about 23 seconds).
    """
    # Execution time: ~ 23 seconds
    nb_total = int(46*45*44/2)
    nb_win = 0
    known_cards = hole_cards + flop_turn
    count = 0
    for river in CARDS:
        if not river in known_cards:
            cat_val_1 = best_cat_feat(known_cards + [river])
            for card_1, card_2 in CARD_PAIRS:
                if (not card_1 in known_cards and not card_2 in known_cards and
                    not river in [card_1, card_2]):
                    cat_val_2 = best_cat_feat([card_1, card_2, river] + flop_turn)
                    if cat_val_1 > cat_val_2:
                        nb_win += 1
                    elif cat_val_1 == cat_val_2:
                        nb_win += 0.5
                    count += 1
    return nb_win/nb_total

#print(prob_win_turn(hc, ft))

def prob_win_turn_Monte_Carlo(hole_cards, flop_turn, proportion=0.1, with_replacement=True):
    """
    Approximation of the probability that player 1 wins knowing his cards, the flop, and the turn.
    """
    # Execution time: ~ 5 seconds
    nb_total = int(46*45*44/2)
    N = int(proportion*nb_total)
    nb_win = 0
    known_cards = hole_cards + flop_turn
    possible_rivers_hole_cards = [(r, list(hc)) for r in CARDS for hc in CARD_PAIRS
                                  if not r in hc and not hc[0] in known_cards
                                  and not hc[1] in known_cards]
    if with_replacement:
        indices = rd.choices(range(nb_total), k = N)
    else:
        indices = rd.sample(range(nb_total), N)
    for i in indices:
        river, hole_cards_2 = possible_rivers_hole_cards[i]
        cat_val_1 = best_cat_feat(hole_cards + flop_turn + [river])
        cat_val_2 = best_cat_feat(hole_cards_2 + flop_turn + [river])
        if cat_val_1 > cat_val_2:
            nb_win += 1
        elif cat_val_1 == cat_val_2:
            nb_win += 0.5
    return nb_win/N

#print(prob_win_turn_Monte_Carlo(hc, ft))


def prob_win_flop_Monte_Carlo(hole_cards, flop, proportion=0.005, with_replacement=True):
    """
    Approximation of the probability that player 1 wins knowing his cards and the flop.
    """
    # Execution time: ~ 10 seconds
    nb_total = int(47*46*45*44/4)
    N = int(proportion*nb_total)
    nb_win = 0
    known_cards = hole_cards + flop
    
    possible_turns_rivers_hole_cards = [(list(tr), list(hc)) for tr in CARD_PAIRS for hc in CARD_PAIRS
                                        if not hc[0] in known_cards and not hc[0] in tr
                                        and not hc[1] in known_cards and not hc[1] in tr
                                        and not tr[0] in known_cards and not tr[0] in hc
                                        and not tr[1] in known_cards and not tr[1] in hc]
    if with_replacement:
        indices = rd.choices(range(nb_total), k = N)
    else:
        indices = rd.sample(range(nb_total), N)
    count = 0
    for i in indices:
        turn_river, hole_cards_2 = possible_turns_rivers_hole_cards[i]
        cat_val_1 = best_cat_feat(hole_cards + flop + turn_river)
        cat_val_2 = best_cat_feat(hole_cards_2 + flop + turn_river)
        if cat_val_1 > cat_val_2:
            nb_win += 1
        elif cat_val_1 == cat_val_2:
            nb_win += 0.5
#        if count%500 == 0:
#            print(round(count/N, 2))
        count += 1
    return nb_win/N

#print(prob_win_flop_Monte_Carlo(hc_1, flp))



"""
OPPONENT CARDS KNOWN
"""


def prob_win_all_known(hole_cards_1, hole_cards_2, flop_turn_river):
    """
    Returns 1 if player 1 wins, 0 if player 1 looses, 0.5 if it is a draw.
    """
    cat_val_1 = best_cat_feat(hole_cards_1 + flop_turn_river)
    cat_val_2 = best_cat_feat(hole_cards_2 + flop_turn_river)
    if cat_val_1 > cat_val_2:
        return 1
    if cat_val_1 == cat_val_2:
        return 0.5
    return 0
    
#print(prob_win_all_known(hc_2, hc_1, ftr))


def prob_win_turn_opponent_known(hole_cards_1, hole_cards_2, flop_turn):
    """
    Probability that player 1 wins knowing his cards, the opponent's cards, the flop, and the turn.
    """
    nb_total = 44
    nb_win = 0
    known_cards = hole_cards_1 + hole_cards_2 + flop_turn
    for river in CARDS:
        if not river in known_cards:
            cat_val_1 = best_cat_feat(hole_cards_1 + flop_turn + [river])
            cat_val_2 = best_cat_feat(hole_cards_2 + flop_turn + [river])
            if cat_val_1 > cat_val_2:
                nb_win += 1
            elif cat_val_1 == cat_val_2:
                nb_win += 0.5
    return nb_win/nb_total

#print(prob_win_turn_opponent_known(hc_1, hc_2, ft))


def prob_win_flop_opponent_known(hole_cards_1, hole_cards_2, flop):
    """
    Probability that player 1 wins knowing his cards, the opponent's cards, and the flop.
    """
    nb_total = int(45*44/2)
    nb_win_1 = 0
    known_cards = hole_cards_1 + hole_cards_2 + flop
    possible_turns_rivers = [list(tr) for tr in CARD_PAIRS if not tr[0] in known_cards
                             and not tr[1] in known_cards]

    for turn_river in possible_turns_rivers:
        cat_val_1 = best_cat_feat(hole_cards_1 + flop + turn_river)
        cat_val_2 = best_cat_feat(hole_cards_2 + flop + turn_river)
        if cat_val_1 > cat_val_2:
            nb_win_1 += 1
        elif cat_val_1 == cat_val_2:
            nb_win_1 += 0.5
    return nb_win_1/nb_total

#prob_win_flop_opponent_known(hc_1, hc_2, flp)


def prob_win_preflop_opponent_known_Monte_Carlo(hole_cards_1, hole_cards_2,
                                                proportion=0.005, with_replacement=True):
    """
    Probability that player 1 wins knowing his cards and the opponent's cards.
    """
    nb_total = int(48*47*46*45*44/120)
    N = int(proportion*nb_total)
    nb_win_1 = 0
    if with_replacement:
        indices = rd.choices(range(nb_total), k = N)
    else:
        indices = rd.sample(range(nb_total), N)
    card_1_a, card_1_b = hole_cards_1
    card_2_a, card_2_b = hole_cards_2
    possible_table_cards = [list(table_cards) for table_cards in FIVE_CARD_SETS if
                            not card_1_a in table_cards and
                            not card_1_a in table_cards and
                            not card_2_b in table_cards and
                            not card_2_b in table_cards]
    count = 0
    for i in indices:
        table_cards = possible_table_cards[i]
        cat_val_1 = best_cat_feat(hole_cards_1 + table_cards)
        cat_val_2 = best_cat_feat(hole_cards_2 + table_cards)
        if cat_val_1 > cat_val_2:
            nb_win_1 += 1
        elif cat_val_1 == cat_val_2:
            nb_win_1 += 0.5
        count += 1
#        if count%500 == 1:
#            print(round(count/N, 2))
    return nb_win_1/N

#print(prob_win_preflop_opponent_known_Monte_Carlo(hc_1, hc_2))



"""
General function
"""


def prob_win(nine_cards):
    """
    Returns the exact value or an approximation of the probability that player 1 wins.
    """
    hole_cards_1 = nine_cards[:2]
    hole_cards_2 = nine_cards[2:4]
    flop = nine_cards[4:7]
    turn = nine_cards[7]
    river = nine_cards[8]
    # if the cards of the opponent are unknown
    if 52 in hole_cards_2:
        # if only the flop is on the table
        if turn == 52:
            return prob_win_flop_Monte_Carlo(hole_cards_1, flop)
        # if only the flop and the turn is on the table
        if river == 52:
            return prob_win_turn_Monte_Carlo(hole_cards_1, flop + [turn])
        # if all five cards are on the table
        return prob_win_river(hole_cards_1, flop + [turn, river])
    # if the cards of the opponent are known
    # if no cards are on the table
    if 52 in flop:
        return prob_win_preflop_opponent_known_Monte_Carlo(hole_cards_1, hole_cards_2)
    # if only the flop is on the table
    if turn == 52:
        return prob_win_flop_opponent_known(hole_cards_1, hole_cards_2, flop)
    # if only the flop and the turn is on the table
    if river == 52:
        return prob_win_turn_opponent_known(hole_cards_1, hole_cards_2, flop + [turn])
    # if all five cards are on the table
    return prob_win_all_known(hole_cards_1, hole_cards_2, flop + [turn, river])
    



"""
MAKE UNITESTS
"""
        
#high_card_1 = "5d 6s 12d 3h 13h"
#high_card_2 = "5d 7s 12d 3h 14h"
#
#print(compare(high_card_1, high_card_2))
#
#pair_1 = "5d 6s 5d 3h 13h"
#pair_2 = "5d 6s 13d 3h 13h"
#
#print(compare(pair_1, pair_2))
#
#db_pair_1 = "5d 6s 5d 6h 13h"
#db_pair_2 = "7d 6s 5d 6h 7h"
#
#print(compare(db_pair_1, db_pair_2))
#
#three_of_kind_1 = "5d 5s 5d 6h 13h"
#three_of_kind_2 = "5d 6s 5d 6h 6c"
#
#print(compare(three_of_kind_1, three_of_kind_2))
#
#straight_1 = "7s 4h 5d 6h 3s"
#straight_2 = "2s 4h 5d 14h 3s"
#
#print(compare(straight_1, straight_2))
#
#flush_1 = "5h 6h 12h 4h 13h"
#flush_2 = "5d 6d 12d 3d 13d"
#
#print(compare(flush_1, flush_2))
#
#full_house_1 = "5d 6s 5d 6h 6c"
#full_house_2 = "5d 5s 6d 6h 5h"
#
#print(compare(full_house_1, full_house_2))
#
#four_of_kind_1 = "5d 5s 5d 5h 13h"
#four_of_kind_2 = "5d 5s 5d 5h 6h"
#
#print(compare(four_of_kind_1, four_of_kind_2))
#
#straight_flush_1 = "7s 4s 5s 6s 3s"
#straight_flush_2 = "12d 14d 10d 11d 13d"
#
#print(compare(straight_flush_1, straight_flush_2))
#
#hand = "5d 13s 8d 5s 14h"
#hand2 = "6s 13s 8s 5s 14d"
#hist_rks, hist_sts = histograms(hand)
#
#print(hist_rks)
#print(hist_sts)
#
#print([rk + 2 for rk in decr_indices(1, hist_rks)])
#print([rk + 2 for nb in [4, 3, 2, 1] for rk in decr_indices(nb, hist_rks)])



