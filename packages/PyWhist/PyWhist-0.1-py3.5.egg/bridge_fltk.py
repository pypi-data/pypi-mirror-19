#!/usr/bin/python3

# (c) 2016 Andrew Warshall. This file is under the terms of the
# Eclipse Public License.

import multiprocessing
from fltk import *
from bridge_util import Card, suit_real, Suit, suit_all, Bid, Bids
from bridge_util import outrank
from time import sleep

class Gui:
    def __init__(self, conn):
        self.conn = conn
        top = self.top = Fl_Window(600, 420, 'PyWhist')
        self.table = Fl_Box(250, 170, 100, 80)
        self.table.box(FL_UP_BOX)
        self.table.color(FL_BLUE)
        hl = Fl_Box(250, 250, 60, 20, 'South')
        scoreboard = self.scoreboard = Fl_Box(0, 0, 100, 140)
        tl = Fl_Box(0, 0, 100, 20, 'Tricks')
        tl.box(FL_UP_BOX)
        self.ts = ''
        tricks = self.tricks = Fl_Box(0, 20, 100, 20, self.ts)
        self.cs = ''
        con = self.con = Fl_Box(0, 40, 100, 20, self.cs)
        gl = Fl_Box(0, 60, 100, 20, 'GmScr')
        gl.box(FL_UP_BOX)
        self.gss = '0--0'
        gs = self.gs = Fl_Box(0, 80, 100, 20, self.gss)
        sl = Fl_Box(0, 100, 100, 20, 'Score')
        sl.box(FL_UP_BOX)
        self.scores = '0--0'
        score = self.score = Fl_Box(0, 120, 100, 20, self.scores)
        top.end()
        top.show()
        Fl.add_fd(self.conn.fileno(), check_pipe, self)
        self.rscore = [0, 0]
        self.bidwin = Fl_Window(150, 170, 'Bids')
        self.bbutts = set()
        pb = self.pb = Fl_Button(0, 0, 45, 30, 'Pass')
        pb.bid = Bids.Pass
        db = self.db = Fl_Button(68, 0, 30, 30, 'Dbl')
        db.bid = Bids.Double
        rb = self.rb = Fl_Button(120, 0, 30, 30, 'Rdbl')
        rb.bid = Bids.Redouble
        self.bbutts.update({pb, db, rb})
        for i in range(1, 8):
            j = 0
            for s in suit_all():
                ss = suit_chr(s)
                bb = Fl_Button(j, 20*i+10, 30, 20, str(i)+ss[0])
                bb.labelcolor(ss[1])
                bb.bid = Bid(i, s)
                self.bbutts.add(bb)
                j += 30
        for b in self.bbutts:
            b.callback(lambda b, x=self: x.make_bid(b.bid))
            b.when(FL_WHEN_NEVER)
        self.bidwin.callback(lambda a, x=self: x.make_bid(Bids.Pass))
        self.bidwin.end()
        self.vul = [False, False]
        Fl.run()

    def show_deal(self, hand, me, dealer):
        self.cards = [set(c for c in hand if c.suit == i)
                      for i in range(4)]
        self.me = me
        self.dummy = None
        self.partner = (self.me+2)%4
        self.suit_order = [Suit.Spades, Suit.Hearts, Suit.Diamonds,
                           Suit.Clubs]
        self.cbutts = {s: [] for s in suit_real()}
        hand_bod = self.hand_bod = Fl_Group(250, 270, 350, 120)
        self.top.add(hand_bod)
        self._show_cards(hand, hand_bod, self.cbutts, True)
        self.shown = set()
        self.bidwin.show()
        self.cs = ''
        self.ts = ''
        self.con.label(self.cs)
        self.tricks.label(self.ts)
        self.top.redraw()

    def _show_cards(self, hand, where, cbutts, mine):
        cards = {s: set(c for c in hand if c.suit is s)
                 for s in suit_real()}
        suits = dict()
        if mine:
            self.suits = suits
        else:
            self.dsuits = suits
        where.begin()
        bot = where.y()
        ctemp = dict()
        for i in self.suit_order:
            sc = suit_chr(i)
            suits[i] = Fl_Pack(where.x()+20, bot, 370, 30, sc[0])
            suits[i].labelcolor(sc[1])
            suits[i].align(FL_ALIGN_LEFT)
            suits[i].type(Fl_Pack.HORIZONTAL)
            ctemp[i] = sorted(cards[i], reverse = True)
            for j in ctemp[i]:
                rs = rank_chr(j.rank)
                c = Fl_Button(0, 0, 25, 30, rs)
                cbutts[i].append(c)
                c.labelcolor(sc[1])
                c.card = j
                c.callback(lambda c, x=self, y=mine:
                           x.choose_card(c, y))
                c.when(FL_WHEN_NEVER)
            suits[i].end()
            bot += 30

    def ask_bid(self, con, last_bid):
        if con.n is not None and con.doubled and not con.redoubled:
            last_bid += 1
        for b in self.bbutts:
            if outrank(b.bid, con, (last_bid-self.me)%2):
                b.when(FL_WHEN_RELEASE)
        self._show(0)

    def make_bid(self, bid):
        for b in self.bbutts:
            b.when(FL_WHEN_NEVER)
        self.conn.send(bid)

    def show_con(self, con, declarer):
        self.bidwin.hide()
        self.tricks.label('0―0')
        ss = suit_chr(con.suit)
        if con.redoubled:
            ds = 'R'
        elif con.doubled:
            ds = 'D'
        else:
            ds = ''
        self.cs = str(con.n)+ss[0]+ds
        self.con.label(self.cs)
        self.con.labelcolor(ss[1])
        self._update_order(con.suit)
        bot = 270
        for i in self.suit_order:
            self.suits[i].position(270, bot)
            bot += 30
        for w in list(self.shown):
            self.top.remove(w)
            self.shown.remove(w)
        self.top.redraw()
        self.declarer = self.me == declarer

    def show_dum(self, dum_hand, dummy):
        self.dummy = dummy
        dpos = (dummy-self.me)%4
        if dpos == 0:
            self.dstr = 'South'
            self.dbutts = self.cbutts
            return
        elif dpos == 1:
            self.dstr = 'West'
            x, y = 0, 140
        elif dpos == 2:
            self.dstr = 'North'
            x, y = 250, 0
        else:
            self.dstr = 'East'
            x, y = 352, 120
        self.top.begin()
        dhead = self.dhead = Fl_Box(x, y, 60, 20, self.dstr)
        dbod = self.dbod = Fl_Group(x, y+20, 350, 120)
        self.dbutts = {s: [] for s in suit_real()}
        self._show_cards(dum_hand, dbod, self.dbutts, False)
        self.top.end()
        self.top.redraw()

    def _update_order(self, trump_suit):
        if trump_suit in {Suit.Spades, Suit.NT}:
            self.suit_order = [Suit.Spades, Suit.Hearts, Suit.Clubs,
                               Suit.Diamonds]
        elif trump_suit is Suit.Hearts:
            self.suit_order = [Suit.Hearts, Suit.Spades, Suit.Diamonds,
                               Suit.Clubs]
        elif trump_suit is Suit.Diamonds:
            self.suit_order = [Suit.Diamonds, Suit.Spades, Suit.Hearts,
                               Suit.Clubs]
        else:
            self.suit_order = [Suit.Clubs, Suit.Hearts, Suit.Spades,
                               Suit.Diamonds]

    def show_card(self, trick, card):
        put_card(self._show((trick.cur_player-self.me)%4, 0), card)
        if trick.cur_player == self.dummy and not self.declarer:
            for cb in self.dbutts[card.suit]:
                if cb.card == card:
                    if self.me != self.dummy:
                        self.dsuits[card.suit].remove(cb)
                    else:
                        self.suits[card.suit].remove(cb)
                    self.dbutts[card.suit].remove(cb)

    def show_bid(self, who, bid):
        put_card(self._show((who-self.me)%4, 0), bid)

    def _show(self, pos, card=None):
        if card is not None:
            if pos == 0:
                l = Fl_Box(285, 230, 30, 20)
            elif pos == 1:
                l = Fl_Box(250, 200, 30, 20)
            elif pos == 2:
                l = Fl_Box(285, 170, 30, 20)
            else:
                l = Fl_Box(320, 200, 30, 20)
            self.top.add(l)
            self.shown.add(l)
            l.box(FL_THIN_UP_BOX)
            l.pos = pos
        else:
            l = None
        sh = list(self.shown)
        for w in sh:
            if w.pos == pos and w is not l:
                self.top.remove(w)
                self.shown.remove(w)
        self.top.redraw()
        return l

    def ask(self, trick, who):
        if who == self.me:
            cbutts = self.cbutts
        else:
            cbutts = self.dbutts
        for s in suit_real():
            if (trick.lead_suit is None or s is trick.lead_suit
                or len(cbutts[trick.lead_suit]) == 0):
                for c in cbutts[s]:
                    c.when(FL_WHEN_RELEASE)

    def choose_card(self, cbutt, mine):
        if mine:
            cbutts = self.cbutts
            suits = self.suits
        else:
            cbutts = self.dbutts
            suits = self.dsuits
        for i in suit_real():
            for c in cbutts[i]:
                c.when(FL_WHEN_NEVER)
        suits[cbutt.card.suit].remove(cbutt)
        self.top.redraw()
        cbutts[cbutt.card.suit].remove(cbutt)
        self.conn.send(cbutt.card)

    def wait_butt(self, func):
        Fl.remove_fd(self.conn.fileno())
        butt = Fl_Button(290, 200, 20, 20, '×')
        butt.callback(func)
        self.top.add(butt)
        butt.redraw()

    def show_trick(self):
        self.wait_butt(self.clear_table)

    def clear_table(self, c):
        self.top.remove(c)
        for l in self.shown:
            self.top.remove(l)
        self.shown.clear()
        self.top.redraw()
        Fl.add_fd(self.conn.fileno(), check_pipe, self)

    def show_score(self, trick_score):
        self.ts = '{}―{}'.format(*trick_score)
        self.tricks.label(self.ts)

    def show_hand(self):
        self.wait_butt(self.clear_hand)

    def clear_hand(self, c):
        self.top.remove(c)
        self.top.remove(self.hand_bod)
        if hasattr(self, 'dhead'):
            self.top.remove(self.dhead)
            self.top.remove(self.dbod)
            self.dummy = None
        self.suits.clear()
        self.top.redraw()
        Fl.add_fd(self.conn.fileno(), check_pipe, self)

    def show_misdeal(self):
        self.wait_butt(self._show_misdeal)

    def _show_misdeal(self, c):
        self.clear_hand(c)
        self.clear_table(c)
        self.bidwin.hide()

    def show_game_score(self, game_score, rubber_score):
        self.gss = '{}–{}'.format(*game_score)
        self.gs.label(self.gss)
        rs0 = game_score[0]+rubber_score[0]
        rs1 = game_score[1]+rubber_score[1]
        if self.vul[0]:
            if self.vul[1]:
                self.scores = '{}↔{}'.format(rs0, rs1)
            else:
                self.scores = '{}←{}'.format(rs0, rs1)
        elif self.vul[1]:
            self.scores = '{}→{}'.format(rs0, rs1)
        else:
            self.scores = '{}–{}'.format(rs0, rs1)
        self.score.label(self.scores)

    def show_rubber_score(self, rubber_score, vul):
        self.rscore = rubber_score
        self.vul = vul
        self.show_game_score([0, 0], rubber_score)

    def congratulate(self, rub_score):
        self.fin('You win, {0[0]}–{0[1]}!'.format(rub_score))

    def console(self, rub_score):
        self.fin('You lose, {0[0]}–{0[1]}!'.format(rub_score))

    def sister(self, rub_score):
        self.fin('You tie, {0}–{0}.'.format(rub_score[0]))

    def fin(self, msg):
        self.msg = msg
        self.f = Fl_Box(150, 0, 300, 48, self.msg)
        self.top.add(self.f)
        self.top.redraw()


def put_card(box, card):
    if isinstance(card, Bids):
        ss = str(card)
        sc = FL_DARK_GREEN
    elif isinstance(card, Bid):
        ss, sc = suit_chr(card.suit)
        ss = str(card.n)+ss
    else:
        ss, sc = suit_chr(card.suit)
        ss = rank_chr(card.rank)+ss
    box.label(ss)
    box.labelcolor(sc)
    box.redraw()

def rank_chr(rank):
    if rank < 8:
        return str(rank+2)
    elif rank == 8:
        return 'T'
    elif rank == 9:
        return 'J'
    elif rank == 10:
        return 'Q'
    elif rank == 11:
        return 'K'
    else:
        return 'A'

def suit_chr(suit):
    if suit is Suit.Clubs:
        return '♣', FL_BLACK
    elif suit is Suit.Diamonds:
        return '♦', FL_MAGENTA
    elif suit is Suit.Hearts:
        return '♥', FL_RED
    elif suit is Suit.Spades:
        return '♠', FL_DARK_BLUE
    else:
        return 'NT', FL_DARK_GREEN

def check_pipe(fd, gui):
    msg = gui.conn.recv()
    getattr(gui, msg[0])(*msg[1:])
