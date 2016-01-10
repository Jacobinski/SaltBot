#TODO: Docstrings
import time
from selenium import webdriver

time_elapsed = 0
driver = webdriver.Firefox()    #Opens firefox
driver.get('http://saltybet.com')

#These are full tag elements ie. <element> text </element>
player1 = driver.find_element_by_id('player1')
player2 = driver.find_element_by_id('player2')
bet_status = driver.find_element_by_id('betstatus')

#Ensure we are in the betting round
while bet_status.text != "Bets are OPEN!":
    time_elapsed += 10
    time.sleep(10)
    print('Sleeping for %s seconds' %time_elapsed)

#Processes attributes of the elements
print(bet_status.text)
print('Player 1: ', player1.get_attribute('value'))
print ('Player 2: ', player2.get_attribute('value'))

driver.close()

#Further Reading:
#http://koaning.io/dynamic-scraping-with-python.html
