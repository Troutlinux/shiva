import requests


class TCLookup(object):
    def __init__(self):

    def lookup_file_ticker(self, emailbody):
        try:
            with open('mytickers.txt') as myfile:
              if 'emailbody' in myfile.read():
                return True
        except Exception as e:
            print(e)
