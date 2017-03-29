#broken *************


import json
import requests
from bs4 import BeautifulSoup

#step 1 lets create class to get solutions from hrank

class hrank:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.accepted_solutions = []

    def get_solutions(self):
        session = requests.Session()