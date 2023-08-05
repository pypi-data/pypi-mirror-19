#!/usr/bin/python3

# (c) 2016 Andrew Warshall. This file is under the terms of the
# Eclipse Public License.

import multiprocessing
try:
    from bridge_fltk import Gui
except ImportError:
    from bridge_tk import Gui

class Hum:
    def __init__(self):
        self.eng_conn, gui_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target = gui_start,
                                         args = (gui_conn,))
        self.p.start()

    def show_deal(self, hand, me, dealer):
        self.eng_conn.send(('show_deal', hand, me, dealer))

    def show_card(self, trick, card):
        self.eng_conn.send(('show_card', trick, card))

    def show_bid(self, who, bid):
        self.eng_conn.send(('show_bid', who, bid))

    def ask_bid(self, con, last_bid):
        self.eng_conn.send(('ask_bid', con, last_bid))
        return self.eng_conn.recv()

    def ask(self, trick, who):
        self.eng_conn.send(('ask', trick, who))
        return self.eng_conn.recv()

    def show_con(self, con, declarer):
        self.eng_conn.send(('show_con', con, declarer))

    def show_misdeal(self):
        self.eng_conn.send(('show_misdeal',))

    def show_trick(self, trick):
        self.eng_conn.send(('show_trick',))

    def show_score(self, trick_score):
        self.eng_conn.send(('show_score', trick_score))

    def show_hand(self):
        self.eng_conn.send(('show_hand',))

    def show_dum(self, dum_hand, dummy):
        self.eng_conn.send(('show_dum', dum_hand, dummy))

    def show_game_score(self, game_score, rubber_score):
        self.eng_conn.send(('show_game_score', game_score,
                            rubber_score))

    def show_rubber_score(self, rubber_score, vul):
        self.eng_conn.send(('show_rubber_score', rubber_score, vul))

    def congratulate(self, rub_score):
        self.eng_conn.send(('congratulate', rub_score))
        self.p.join()
        quit()

    def console(self, rub_score):
        self.eng_conn.send(('console', rub_score))
        self.p.join()
        quit()

    def sister(self, rub_score):
        self.eng_conn.send(('sister', rub_score))
        self.p.join()
        quit()


def gui_start(conn):
    g = Gui(conn)
