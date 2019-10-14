import bs4 as bs
import pickle
import pprint
import requests


class CountryCodes:

    def __init__(self):
        self.codes = self.load_codes()
        self.categories = self.load_categories() 

    def load_codes(self):
        with open('country_codes.pickle', 'rb') as f:
            return pickle.load(f)

    def load_alt_codes(cls, pickle_file):
        with open(pickle_file, 'rb') as f:
            self.codes = pickle.load(f)

    @property
    def countries(self):
        pprint.pprint(self.codes)
