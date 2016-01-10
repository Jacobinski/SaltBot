#TODO: Docstrings
import ast

'''This class is a database for categorizing characters in the SaltyBet-Bot system. It holds an internal representation
of all contestants and is able to export its list of characters to an external source text file.
'''
class Database:

    __database_dictionary = None

    #Constructor
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            s = f.read()
            self.__database_dictionary = ast.literal_eval(s) #String -> Dictionary. Safe method which only creates primitives

    def write_database(self):
