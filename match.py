'''
The match monitoring module for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time

from website import website

class Match:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.duration = None
        self.winner = None
        self.p1bets = None
        self.p2bets = None
        self.mybet = None
        self.myplayer = None

    def start_round(self, myplayer, mybet, website):
        self.player1 = website.get_player1_name()
        self.player2 = website.get_player2_name()
        self.p1bets = website.get_player1_wagers()
        self.p2bets = website.get_player2_wagers()
        self.mybet = mybet
        self.myplayer = myplayer

    def end_round(self, duration, winner):
        self.duration = duration
        self.winner = winner

    def save_round(self):
        # TODO: Save to SQL
        return

def record_match(session, request):
    """
    Places bets on SaltyBet matches.

    Runs the logic of SaltBot. Periodically scrapes and places bets on
    the website.

    Args:
        session (session): A requests library session.
        request (request): A requests library request.

    Returns:
        None

    Todo:
        * Logic should go into main.
        * This function should record matches to a database.

    """

    # Empty for now
    pass

