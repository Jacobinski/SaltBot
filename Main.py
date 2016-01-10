from selenium import webdriver

driver = webdriver.Firefox()    #Opens firefox
driver.get('http://saltybet.com')

player1 = driver.find_element_by_id("player1")
player2 = driver.find_element_by_id("player2")

print (player2.get_attribute('value'))

driver.close()

#Further Reading:
#http://koaning.io/dynamic-scraping-with-python.html
