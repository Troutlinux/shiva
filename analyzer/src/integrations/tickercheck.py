import requests


class TCLookup(object):
    #def __init__(self):

    def validate_if_it_contains_ticker(self, word):
        try:
            with open('analyzer/integrations/tickers.txt') as myfile:
              print(f"Checking for word: {word}")
              if word in myfile.read():
                print("A ticker was found!")
                return True
        except Exception as e:
            print(e)
