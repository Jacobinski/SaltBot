"""
A class for emulating a Firefox web browser on www.saltybet.com.
"""
#TODO: https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example
#TODO: Tournament mode and such
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WebBrowser:

    driver = None
    time_elapsed = None

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

    def getPlayers(self):  # Returns a map
        # These are full tag elements ie. <element> text </element>
        player1 = self.driver.find_element_by_id('player1')
        player2 = self.driver.find_element_by_id('player2')
        wait = WebDriverWait(self.driver, 1800)  # Wait 30 minutes
        wait.until(EC.text_to_be_present_in_element((By.ID, 'betstatus'), "Bets are OPEN!")) #Wait until bet round
        output = {'player1': player1.get_attribute('value'),
                  'player2': player2.get_attribute('value')}
        return output

    def getMatchTime(self):
        #TODO

    def getWinner(self):
        #TODO
        #Payouts to Team Red. -> Player1
        #Payouts to Team Blue. -> Player2


    def getBalance(self):
        dollar = self.driver.find_element_by_class_name('dollar')
        return int(dollar.text[1:])

    def bet(self, player, balance): #player is 'player1' | 'player2'
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

    def end(self):
            self.driver.close()

# Further Reading:
# http://koaning.io/dynamic-scraping-with-python.html -> Make firefox not actually open
