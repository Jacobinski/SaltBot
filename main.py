'''
A python script for SaltBot
'''
from login import saltbot_login
from match import record_match

def main():
    """
    The main run loop for SaltBot

    """

    # Login to SaltyBet
    session, request = saltbot_login()

    # Record the match
    record_match(session, request)

if __name__ == '__main__':
    main()