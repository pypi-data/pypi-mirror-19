#!/usr/bin/python3

# (c) 2016 Andrew Warshall. This file is under the terms of the
# Eclipse Public License.

import multiprocessing
import tkinter
from bridge_util import Card, suit_real, Suit, suit_all, Bid, Bids
from bridge_util import outrank

class Gui:
    def __init__(self, conn):
        self.conn = conn
        top = self.top = tkinter.Tk()
        w = self.w = tkinter.Canvas(top, height = 400, width = 600)
        w.pack()
        self.table = tkinter.Canvas(w, bd = 2, relief = 'raised',
                                    bg = 'blue', height = 60,
                                    width = 100)
        w.create_window(300, 200, window = self.table)
        hand = self.hand = tkinter.Frame(w)
        hand_head = tkinter.Label(self.hand, text = 'South')
        hand_head.pack()
        hand_bod = self.hand_bod = tkinter.Frame(self.hand)
        hand_bod.pack()
        w.create_window(250, 232, anchor = 'nw', window = hand)
        scoreboard = self.scoreboard = tkinter.Frame(w, height = 140,
                                                     width = 100,
                                                     bg = 'red')
        w.create_window(0, 0, anchor = 'nw', window = scoreboard)
        tl = tkinter.Label(scoreboard, text = 'Tricks', bg = 'red')
        tl.pack()
        tricks = self.tricks = tkinter.Label(scoreboard)
        tricks.pack()
        con = self.con = tkinter.Label(scoreboard)
        con.pack()
        gl = tkinter.Label(scoreboard, text = 'GmScr', bg = 'red')
        gl.pack()
        gs = self.gs = tkinter.Label(scoreboard, text = '0--0')
        gs.pack()
        sl = tkinter.Label(scoreboard, text = 'Score', bg = 'red')
        sl.pack()
        score = tkinter.Frame(scoreboard)
        score.pack()
        s1 = self.s1 = tkinter.Label(score, text = '0')
        s1.pack(side = 'left')
        tkinter.Label(score, text = '--').pack(side = 'left')
        s2 = self.s2 = tkinter.Label(score, text = '0')
        s2.pack(side = 'left')
        top.after(100, self.check_pipe)
        top.mainloop()

    def check_pipe(self):
        if self.conn.poll():
            msg = self.conn.recv()
            getattr(self, msg[0])(*msg[1:])

    def show_deal(self, hand, me, dealer):
        self.me = me
        self.dummy = None
        self.partner = (self.me+2)%4
        self.suit_order = [Suit.Spades, Suit.Hearts, Suit.Diamonds,
                           Suit.Clubs]
        self.cbutts = {s: [] for s in suit_real()}
        self._show_cards(hand, self.hand_bod, self.cbutts, True)
        self.shown = set()
        self.bidwin = tkinter.Toplevel()
        self.bbutts = set()
        for i in range(1, 8):
            for s in suit_all():
                ss = suit_chr(s)
                bb = tkinter.Button(self.bidwin, text = str(i)+ss[0],
                                    fg = ss[1])
                bb.grid(row=i-1, column=s.value)
                bb.bid = Bid(i, s)
                self.bbutts.add(bb)
        pb = self.pb = tkinter.Button(self.bidwin, text = 'Pass')
        pb.grid(row=7, column=0)
        pb.bid = Bids.Pass
        db = self.db = tkinter.Button(self.bidwin, text = 'Dbl')
        db.grid(row=7, column=1)
        db.bid = Bids.Double
        rb = self.rb = tkinter.Button(self.bidwin, text = 'Rdbl')
        rb.grid(row=7, column=2)
        rb.bid = Bids.Redouble
        self.bbutts.update({pb, db, rb})
        for b in self.bbutts:
            b.config(command = lambda x=b.bid: self.make_bid(x),
                     state = 'disabled')
        self.con.config(text = '')
        self.tricks.config(text = '')
        self.top.after(100, self.check_pipe)

    def _show_cards(self, hand, where, cbutts, mine):
        cards = {s: set(c for c in hand if c.suit is s)
                 for s in suit_real()}
        suits = dict()
        if mine:
            self.suits = suits
        for i in self.suit_order:
            suits[i] = tkinter.Frame(where)
            suits[i].pack(anchor = 'w')
            ss = suit_chr(i)
            l = tkinter.Label(suits[i], bg = 'white', fg = ss[1],
                              text = ss[0])
            l.pack(side = 'left', anchor = 'w')
            ctemp = sorted(cards[i], reverse = True)
            for j in ctemp:
                rs = rank_chr(j.rank)
                cbutts[i].append(tkinter.Button(suits[i], text = rs,
                                 fg = ss[1], width = 1, padx = 2))
                cbutts[i][-1].card = j
                cbutts[i][-1].pack(side = 'left', anchor = 'w')

    def ask_bid(self, con, last_bid):
        if con.n is not None and con.doubled and not con.redoubled:
            last_bid += 1
        for b in self.bbutts:
            if outrank(b.bid, con, (last_bid-self.me)%2):
                b.config(state = 'normal')
        self._show(0)

    def make_bid(self, bid):
        for b in self.bbutts:
            b.config(state = 'disabled')
        self.conn.send(bid)
        self.top.after(100, self.check_pipe)

    def show_con(self, con, declarer):
        self.bidwin.destroy()
        self.tricks.config(text = '0--0')
        ss = suit_chr(con.suit)
        if con.redoubled:
            ds = 'R'
        elif con.doubled:
            ds = 'D'
        else:
            ds = ''
        self.con.config(text=str(con.n)+ss[0]+ds, fg = ss[1])
        self._update_order(con.suit)
        for i in self.suit_order:
            self.suits[i].pack_forget()
        for i in self.suit_order:
            self.suits[i].pack(anchor='w')
        for w in list(self.shown):
            self.table.delete(w.i)
            self.shown.remove(w)
        self.declarer = self.me == declarer
        self.top.after(100, self.check_pipe)

    def show_dum(self, dum_hand, dummy):
        self.dummy = dummy
        dpos = (dummy-self.me)%4
        if dpos == 0:
            self.dstr = 'South'
            self.dbutts = self.cbutts
            self.top.after(100, self.check_pipe)
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
        dhand = self.dhand = tkinter.Frame(self.w)
        dhead = tkinter.Label(self.dhand, text = self.dstr)
        dhead.pack()
        dbod = self.dbod = tkinter.Frame(dhand)
        dbod.pack()
        self.dbutts = {s: [] for s in suit_real()}
        self._show_cards(dum_hand, dbod, self.dbutts, False)
        self.dwin = self.w.create_window(x, y, anchor = 'nw',
                                         window = dhand)
        self.top.after(100, self.check_pipe)

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
        self._show((trick.cur_player-self.me)%4, card)
        if trick.cur_player == self.dummy and not self.declarer:
            for cb in self.dbutts[card.suit]:
                if cb.card == card:
                    cb.pack_forget()
        self.top.after(100, self.check_pipe)

    def show_bid(self, who, bid):
        self._show((who-self.me)%4, bid)
        self.top.after(100, self.check_pipe)

    def _show(self, pos, card=None):
        for w in list(self.shown):
            if w.pos == pos:
                self.table.delete(w.i)
                self.shown.remove(w)
        if card is not None:
            l = tkinter.Label(self.table, **card_str(card))
            self.shown.add(l)
            l.pos = pos
            if pos == 0:
                l.i = self.table.create_window(50, 60, anchor = 's',
                                               window = l)
            elif pos == 1:
                l.i = self.table.create_window(0, 30, anchor = 'w',
                                               window = l)
            elif pos == 2:
                l.i = self.table.create_window(50, 0, anchor = 'n',
                                               window = l)
            else:
                l.i = self.table.create_window(100, 30, anchor = 'e',
                                               window = l)

    def ask(self, trick, who):
        if who == self.me:
            cbutts = self.cbutts
        else:
            cbutts = self.dbutts
        for s in suit_real():
            if (trick.lead_suit is None or s is trick.lead_suit
                or len(cbutts[trick.lead_suit]) == 0):
                for c in cbutts[s]:
                    c.config(command
                             = lambda x=c, y=cbutts:
                               self.choose_card(x, y))

    def choose_card(self, cbutt, cbutts):
        for s in suit_real():
            for c in cbutts[s]:
                c.config(command = lambda : None)
        cbutt.pack_forget()
        cbutts[cbutt.card.suit].remove(cbutt)
        self.conn.send(cbutt.card)
        self.top.after(100, self.check_pipe)

    def show_trick(self):
        self.top.bind('<ButtonRelease>', self.clear_table)

    def show_misdeal(self):
        self.top.bind('<ButtonRelease>', self._show_misdeal)

    def _show_misdeal(self, e):
        self.top.bind('<ButtonRelease>', lambda e: None)
        self._clear_hand()
        self._clear_table()
        self.bidwin.destroy()
        self.top.after(100, self.check_pipe)

    def _clear_table(self):
        for l in self.shown:
            self.table.delete(l.i)
        self.shown.clear()

    def clear_table(self, e):
        self.top.bind('<ButtonRelease>', lambda e: None)
        self._clear_table()
        self.top.after(100, self.check_pipe)

    def show_score(self, trick_score):
        self.tricks.config(text = '{}--{}'.format(*trick_score))
        self.top.after(100, self.check_pipe)

    def show_hand(self):
        self.top.bind('<ButtonRelease>', self.clear_hand)

    def _clear_hand(self):
        for s in self.suit_order:
            self.suits[s].pack_forget()
        self.suits.clear()

    def clear_hand(self, e):
        self.top.bind('<ButtonRelease>', lambda e: None)
        self._clear_hand()
        if hasattr(self, 'dwin'):
            self.w.delete(self.dwin)
        self.top.after(100, self.check_pipe)

    def show_game_score(self, game_score, rubber_score):
        self.gs.config(text = '{0[0]}--{0[1]}'.format(game_score))
        self.s1.config(text = str(rubber_score[0]+game_score[0]))
        self.s2.config(text = str(rubber_score[1]+game_score[1]))
        self.top.after(100, self.check_pipe)

    def show_rubber_score(self, rubber_score, vul):
        if vul[0]:
            self.s1.config(bg = 'red')
        if vul[1]:
            self.s2.config(bg = 'red')
        self.s1.config(text = str(rubber_score[0]))
        self.s2.config(text = str(rubber_score[1]))
        self.gs.config(text = '0--0')
        self.top.after(100, self.check_pipe)

    def congratulate(self, rub_score):
        self.fin('You win, {0[0]}--{0[1]}!'.format(rub_score))

    def console(self, rub_score):
        self.fin('You lose, {0[0]}--{0[1]}!'.format(rub_score))

    def sister(self, rub_score):
        self.fin('You tie, {0}--{0}.'.format(rub_score[0]))

    def fin(self, msg):
        self.w.create_text(300, 0, anchor = 'n', text = msg)
        self.top.bind('<ButtonRelease>', lambda e: quit())


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
        return '♣', 'black'
    elif suit is Suit.Diamonds:
        return '♦', 'deep pink'
    elif suit is Suit.Hearts:
        return '♥', 'red'
    elif suit is Suit.Spades:
        return '♠', 'midnight blue'
    else:
        return 'NT', 'green'

def card_str(card):
    if hasattr(card, 'rank'):
        s, color = suit_chr(card.suit)
        return {'text':rank_chr(card.rank)+s, 'fg':color, 'bg':'white'}
    else:
        bid = card
        if bid is Bids.Pass:
            return {'text':'Pass', 'fg':'white', 'bg':'black'}
        elif bid is Bids.Double:
            return {'text':'Dbl', 'fg':'white', 'bg':'black'}
        elif bid is Bids.Redouble:
            return {'text':'Rdbl', 'fg':'white', 'bg':'black'}
        else:
            s, color = suit_chr(bid.suit)
            return {'text':str(bid.n)+s, 'fg':color, 'bg':'white'}
