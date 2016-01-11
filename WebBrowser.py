"""
A class for emulating a Firefox web browser on www.saltybet.com.
"""
#TODO: https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example
import time
from selenium import webdriver


class WebBrowser:

    def __init__(self):
        self.time_elapsed = 0
        self.driver = webdriver.Firefox()  # Opens Firefox

    def login(self, webpage):
        # Ask the user for Username & Password, then redirect to stream
        self.driver.get(webpage)
        while self.driver.current_url != 'http://www.saltybet.com/':  # Will not proceed until successful login
            email = self.driver.find_element_by_id('email')
            password = self.driver.find_element_by_id('pword')
            submit = self.driver.find_element_by_class_name('graybutton')
            user_email = input('Enter an email: ')
            user_password = input('Enter a password: ')
            email.send_keys(user_email)
            password.send_keys(user_password)
            submit.click()
            if (self.driver.current_url ==
                    'http://www.saltybet.com/authenticate?signin=1&error=Invalid%20Email%20or%20Password'):
                print('Unsuccessful Login. Try Again')
        print('Successful Login')

    def end(self):
        self.driver.close()

    def getPlayers(self):  # Returns a map
        # These are full tag elements ie. <element> text </element>
        player1 = self.driver.find_element_by_id('player1')
        player2 = self.driver.find_element_by_id('player2')
        bet_status = self.driver.find_element_by_id('betstatus') # Determines if bets are open

        # Ensure we are in the betting round
        while bet_status.text != "Bets are OPEN!":
            self.time_elapsed += 10
            time.sleep(10)
            print('Waiting for next match - %s seconds' % self.time_elapsed)

        output = {'player1': player1.get_attribute('value'),
                  'player2': player2.get_attribute('value')}
        return output

    def getBalance(self):
        dollar = self.driver.find_element_by_class_name('dollar')
        return int(dollar.text[1:])

    def selectPlayer(self, player, balance): #player is 'player1' | 'player2'
        player1 = self.driver.find_element_by_id('player1')
        player2 = self.driver.find_element_by_id('player2')
        bet_input = self.driver.find_element_by_id('wager')

        bet_input.send_keys(balance) #Place the bet
        if player == 'player1':
            player1.click()
        elif player == 'player2':
            player2.click()
        else:
            raise ValueError('Non-allowed player name passed to selectPlayer()')

        '''
        # Processes attributes of the elements
        print(bet_status.text)
        print('Player 1: ', player1.get_attribute('value'))
        print('Player 2: ', player2.get_attribute('value'))
        bet_input.send_keys(dollar.text[1:])
        player2.click()
        '''
# Further Reading:
# http://koaning.io/dynamic-scraping-with-python.html
