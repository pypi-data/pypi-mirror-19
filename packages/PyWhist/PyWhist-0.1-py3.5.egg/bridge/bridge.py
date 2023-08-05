#!/usr/bin/python3

# (c) 2016 Andrew Warshall. This file is under the terms of the
# Eclipse Public License.

import random
from bridge_util import Card, has_suit, find_max, winner, Bid, Contract
from bridge_util import Suit, suit_real, rank_str, Bids, val, over_bonus
from bridge_util import under_bonus
from bridge_hum import Hum
from bridge_ai import AI

class Trick:
    def __init__(self, leader, show_dum):
        self.leader = leader
        self.lead_suit = None
        self.cards = [None]*4
        for self.cur_player in (list(range(leader, 4))
                                +list(range(leader))):
            if self.cur_player == dummy:
                if show_dum:
                    for b in brains:
                        b.show_dum(hands[dummy], dummy)
                thinker = (self.cur_player+2)%4
            else:
                thinker = self.cur_player
            while True:
                play = brains[thinker].ask(self, self.cur_player)
                if play in hands[self.cur_player]:
                    if self.cur_player == leader:
                        self.lead_suit = play.suit
                        break
                    if (self.lead_suit == play.suit
                        or not has_suit(hands[self.cur_player],
                                        self.lead_suit)):
                        break
            hands[self.cur_player].remove(play)
            self.cards[self.cur_player] = play
            for b in brains:
                b.show_card(self, play)
        self.winner = winner(self, trump)[0]
        trick_score[self.winner%2] += 1
        for b in brains:
            b.show_trick(self)



def deal():
    '''Shuffle and deal hands. The RNG must be initialized first.
    '''
    global hands
    deck = list(range(52))
    random.shuffle(deck)
    hands = [set(Card(Suit(n%4), n%13) for n in deck[i*13:i*13+13])
             for i in range(4)]

def honors(trump):
    '''Check if either side scores for honors. If N/S does then the
    return value is positive, if E/W then negative, else 0.
    '''
    if trump.is_suit():
        for i, h in enumerate(hands):
            n = len([c for c in h if c.suit == trump and c.rank > 7])
            if n > 3:
                if i%2:
                    if n == 4:
                        return -10
                    else:
                        return -15
                else:
                    if n == 4:
                        return 10
                    else:
                        return 15
        return 0
    else:
        for i, h in enumerate(hands):
            n = len([c for c in h if c.rank == 12])
            if n == 4:
                if i%2:
                    return -15
                else:
                    return 15
        return 0

def print_hand(hand):
    for s in suit_real():
        ch = [rank_str(c.rank) for c in hand if c.suit is s]
        print(s, end=' ')
        for i in ch:
            print(i, end='')
        print()
    print()

def play_hand():
    '''Play one hand. The RNG must be initialized first.
    '''
    global trump, trick_score, declarer, dummy
    trick_score = [0, 0]
    con = Contract()
    deal()
    for i in range(4):
        brains[i].show_deal(hands[i], i, dealer)
    i = dealer
    passes = -1
    declarer = {}
    for s in Suit:
        declarer[s] = [None, None]
    cur_dec = None
    last_bid = 0
    while passes < 3:
        while True:
            b = brains[i].ask_bid(con, last_bid)
            try:
                con.apply(b, (i-last_bid)%2)
            except ValueError:
                pass
            else:
                break
        for br in brains:
            br.show_bid(i, b)
        if b is Bids.Pass:
            passes += 1
        else:
            last_bid = i
            passes = 0
            try:
                fake_suit = (b.suit, i%2)
            except AttributeError:
                pass
            else:
                if declarer[fake_suit[0]][fake_suit[1]] is None:
                    declarer[fake_suit[0]][fake_suit[1]] = i
                cur_dec = declarer[fake_suit[0]][fake_suit[1]]
        if i == 3:
            i = 0
        else:
            i += 1
    for br in brains:
        if cur_dec is None:
            br.show_misdeal()
        else:
            declarer = cur_dec
            br.show_con(con, declarer)
    if cur_dec is not None:
        trump = con.suit
        leader = (declarer+1)%4
        dummy = (leader+1)%4
        honor_score = honors(trump)
        for i in range(13):
            leader = Trick(leader, i == 0).winner
            for b in brains:
                b.show_score(trick_score)
        for b in brains:
            b.show_hand()
        over = trick_score[declarer%2]-6-con.n
        if over >= 0:
            game_score[declarer%2] += val(con)
            rub_score[declarer%2] += over_bonus(over, con,
                                                vul[declarer%2])
        else:
            rub_score[(declarer+1)%2] += under_bonus(-over, con,
                                                     vul[declarer%2])
        if honor_score > 0:
            rub_score[0] += honor_score
        else:
            rub_score[1] -= honor_score

def game_over():
    if rub_score[0] > rub_score[1]:
        brains[0].congratulate(rub_score)
    elif rub_score[0] < rub_score[1]:
        brains[0].console(rub_score)
    else:
        brains[0].sister(rub_score)
    quit()

def main():
    random.seed()
    brains = [Hum(), AI(), AI(), AI()]
    dealer = random.randrange(4)
    game_score = [0, 0]
    rub_score = [0, 0]
    vul = [False, False]
    while True:
        play_hand()
        for b in brains:
            b.show_game_score(game_score, rub_score)
        if game_score[0] >= 10:
            for i in range(2):
                rub_score[i] += game_score[i]
            if vul[0]:
                rub_score[0] += 50 if vul[1] else 70
                game_over()
            else:
                vul[0] = True
            game_score[0] = 0
            game_score[1] = 0
            for b in brains:
                b.show_rubber_score(rub_score, vul)
        elif game_score[1] >= 10:
            for i in range(2):
                rub_score[i] += game_score[i]
            if vul[1]:
                rub_score[1] += 50 if vul[0] else 70
                game_over()
            else:
                vul[1] = True
            game_score[0] = 0
            game_score[1] = 0
            for b in brains:
                b.show_rubber_score(rub_score, vul)
        if dealer < 3:
            dealer += 1
        else:
            dealer = 0
