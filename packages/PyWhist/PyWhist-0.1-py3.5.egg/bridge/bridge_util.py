#!/usr/bin/python3

# (c) 2016 Andrew Warshall. This file is under the terms of the
# Eclipse Public License.

import enum

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.suit is other.suit and self.rank == other.rank

    def __hash__(self):
        return 13*self.suit.value+self.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __str__(self):
        return rank_str(self.rank)+str(self.suit)

def rank_str(n):
    if n == 12:
        return 'A'
    elif n == 11:
        return 'K'
    elif n == 10:
        return 'Q'
    elif n == 9:
        return 'J'
    elif n == 8:
        return 'T'
    else:
        return str(n+2)

def has_suit(hand, suit):
    '''Return True if hand contains any card of suit.
    '''
    return suit in [c.suit for c in hand]

def suit_count(hand, suit):
    '''Return number of cards of hand in suit.
    '''
    return [c.suit for c in hand].count(suit)

def high_card_suit(hand, suit):
    '''Return highest card of hand in given suit, or None if hand is
    void in suit.
    '''
    try:
        return max(c for c in hand if c.suit is suit)
    except ValueError:
        return None

def high_card_suit_b4d(hand, suit, dum_hand):
    '''Return highest card of hand in given suit, taking into account
    that we only need to beat cards in dum_hand, or None if hand is
    void in suit.
    '''
    l = sorted({c for c in hand if c.suit is suit}, reverse = True)
    if len(l) == 0:
        return None
    else:
        last = l[0]
        for c in l[1:]:
            if len({d for d in dum_hand if d.suit is suit
                    and c < d < last}) > 0:
                return last
            else:
                last = c
        return last


def low_card_suit(hand, suit):
    '''Return lowest card of hand in given suit. Raise ValueError if
    hand is void in suit.
    '''
    return min(c for c in hand if c.suit == suit)

def find_max(seq):
    '''Find the index at which sequence seq has its (first) maximum.
    Raise ValueError if seq is empty.
    '''
    return seq.index(max(sequence))

def find_min(seq):
    '''Find the index at which sequence seq has its (first) minimum.
    Raise ValueError if seq is empty.
    '''
    return seq.index(min(sequence))

def low_card_hand(hand, trump):
    '''Return (one of the) lowest card(s) of hand, taking trump into
    account. Raise ValueError if hand is empty.
    '''
    try:
        return min(c for c in hand if c.suit is not trump)
    except ValueError:
        return min(c for c in hand)

def winner(trick, trump):
    '''Return (winner, winning card) of trick with given trump suit.
    Raise ValueError if trick has no cards yet played.
    '''
    try:
        best = max([c for c in trick.cards
                    if c is not None and c.suit is trump])
    except ValueError:
        best = max([c for c in trick.cards
                    if c is not None and c.suit is trick.lead_suit])
    return trick.cards.index(best), best

class Bids(enum.Enum):
    Pass = 0
    Double = 1
    Redouble = 2

    def plus_one(self):
        return self

    def __str__(self):
        if self is Bids.Pass:
            return 'Pass'
        elif self is Bids.Double:
            return 'Dbl'
        else:
            return 'Rdbl'

class Suit(enum.Enum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3
    NT = 4

    def is_major(self):
        return self in {Suit.Hearts, Suit.Spades}

    def is_minor(self):
        return self in {Suit.Diamonds, Suit.Clubs}

    def is_suit(self):
        return self is not Suit.NT

    def prev(self):
        if self.value == 0:
            return Suit.Spades
        else:
            return Suit(self.value-1)

    def next(self):
        return Suit(self.value+1)

    def __str__(self):
        if self is Suit.Clubs:
            return 'C'
        elif self is Suit.Diamonds:
            return 'D'
        elif self is Suit.Hearts:
            return 'H'
        elif self is Suit.Spades:
            return 'S'
        else:
            return 'NT'

def suit_all():
    s = Suit.Clubs
    yield s
    while s is not Suit.NT:
        s = s.next()
        yield s

def suit_real(start = Suit.Spades):
    yield start
    s = start.prev()
    while s is not start:
        yield s
        s = s.prev()

def suit_fwd(start = Suit.Clubs):
    s = start
    while s is not Suit.NT:
        yield s
        s = s.next()

def find_val(d, val):
    for k, v in d.items():
        if v == val:
            return k
    raise ValueError

class Bid:
    def __init__(self, l, s):
        self.n = l
        self.suit = s

    def plus_one(self):
        return Bid(self.n+1, self.suit)

    def next_suit(self):
        if self.suit in (Suit.Spades, Suit.NT):
            return Bid(self.n+1, Suit.Clubs)
        else:
            return Bid(self.n, Suit(self.suit.value+1))

    def __str__(self):
        return str(self.n)+str(self.suit)

def outrank(bid, con, hostile):
    if bid is Bids.Pass:
        return True
    if bid is Bids.Double:
        return con.n is not None and not con.doubled and hostile
    if bid is Bids.Redouble:
        return (con.n is not None and con.doubled
                and not con.redoubled and hostile)
    if con.n is None:
        return True
    return (bid.n > con.n
            or (bid.n == con.n and bid.suit.value > con.suit.value))

class Contract:
    def __init__(self):
        self.n = None

    def apply(self, bid, hostile):
        if not outrank(bid, self, hostile):
            raise ValueError
        if bid is Bids.Double:
            self.doubled = True
        elif bid is Bids.Redouble:
            self.redoubled = True
        elif bid is not Bids.Pass:
            self.n = bid.n
            self.suit = bid.suit
            self.doubled = False
            self.redoubled = False

def val(con):
    if con.suit.is_minor():
        base_val = 2
    else:
        base_val = 3
    base_val *= con.n
    if con.suit is Suit.NT:
        base_val += 1
    if hasattr(con, 'doubled') and con.doubled:
        if con.redoubled:
            base_val *= 4
        else:
            base_val *= 2
    return base_val

def over_bonus(over, con, vul):
    if con.n == 6:
        if vul:
            slam_val = 75
        else:
            slam_val = 50
    elif con.n == 7:
        if vul:
            slam_val = 150
        else:
            slam_val = 100
    else:
        slam_val = 0
    if hasattr(con, 'doubled') and con.doubled:
        slam_val *= 2
        if over > 0:
            val = 20*over-10
        else:
            val = 0
        if vul:
            val *= 2
        val += 5
        if con.redoubled:
            val *= 2
            slam_val *= 2
    else:
        if con.suit.is_minor():
            base_val = 2
        else:
            base_val = 3
        val = base_val*over
    return val+slam_val

def under_bonus(under, con, vul):
    if con.doubled:
        if vul:
            val = 30*under
        else:
            val = 20*under
        val -= 10
        if con.redoubled:
            val *= 2
    else:
        if vul:
            val = 10*under
        else:
            val = 5*under
    return val
