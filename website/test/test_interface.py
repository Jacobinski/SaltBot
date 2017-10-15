import pytest

from authenticate import login
from website import interface

@pytest.fixture(scope="module")
def setup():
    session, request = login()
    return interface(session, request)

def test_get_alert(setup):
    alert = setup.get_alert()
    assert(alert != None)

def test_get_balance(setup):
    balance = setup.get_balance()
    assert(balance != None)
    assert(balance > 0)

def test_get_json(setup):
    json = setup.get_json()
    assert(json != None)

def test_get_player1_name(setup):
    name = setup.get_player1_name()
    assert(name != None)

def test_get_player1_wagers(setup):
    wagers = setup.get_player1_wagers()
    assert(wagers != None)

def test_get_player2_name(setup):
    name = setup.get_player2_name()
    assert(name != None)

def test_get_player2_wagers(setup):
    wagers = setup.get_player2_wagers()
    assert(wagers != None)

def test_remaining(setup):
    remaining = setup.get_remaining()
    assert(remaining != None)

