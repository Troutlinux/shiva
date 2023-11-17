import requests


class TCLookup(object):
    #def __init__(self):

    def validate_if_it_contains_ticker(self, word):
        try:
            with open('tickers.txt') as myfile:
              if 'word' in myfile.read():
                return True
        except Exception as e:
            print(e)
