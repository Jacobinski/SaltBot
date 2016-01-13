#TODO: Docstrings
#TODO: Export characters to a file. Use pickle? http://stackoverflow.com/questions/4529815/saving-an-object-data-persistence-in-python

'''
This class represents a character object for the SaltyBet-Bot System. It is able to store a character's name,
ELO ranking, and confidence. Confidence is a function of matches won and ability of the program to successfully
predict match results. If a name is shared between characters of varying skill levels, the character object will
hold a low confidence score due to varying results.
'''

import pickle


class Character:

    __name = None
    #__confidence = None
    __rating = None

    def __init__(self, name):
        self.name = name
        self.rating = 1000  # Default value

    '''
    def setConfidence(self, confidence):
        self.__confidence = confidence

    def getConfidence(self):
        return self.__confidence
    '''

    #Get tier -> These will be added during tournaments
    # '<p class="bettor-line"><span class="goldtext">Tier </span>' + p2tier + '</p>' -> THis is in the source file for tournaments and betting and such
    #A player can move up or down a tier by winning or losing 10 matches in a row
    #www-cdn-jtvnw-x.js is the java file which will help me determine tournament status

    def setRating(self, rating):
        self.__rating = rating

    def getRating(self):
        return self.__rating

    def getName(self):
        return self.__name
