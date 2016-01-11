"""
The main executing file in the SaltyBet Bot program. Controls the operation of all other submodules
"""

import time
from WebBrowser import WebBrowser

browser = WebBrowser()
browser.login('http://www.saltybet.com/authenticate?signin=1')
players = browser.getPlayers()
balance = browser.getBalance()
browser.selectPlayer('player1', balance/4)
print("P1:", players.get('player1'))
print("P2:", players.get('player2'))
print("%i placed on %s" %(balance/4, players.get('player1')))

browser.end()

