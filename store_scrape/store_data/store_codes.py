import bs4 as bs
import os
from pathlib import Path
import pickle
import pprint
import requests


project_base = Path(__file__).resolve().parent.parent
store_data = project_base.joinpath('store_data')

class CountryCodes:
    '''Simple class for loading country information.
    '''

    def __init__(self):
        self.codes = self.load_codes()

    def load_codes(self):
        '''Method for loading country codes from pickle file.
        '''
        with open(store_data.joinpath('country_codes.pickle'), 'rb') as f:
            return pickle.load(f)

    def load_alt_codes(cls, pickle_file):
        '''Method for loading alt. codes.
        '''
        with open(pickle_file, 'rb') as f:
            self.codes = pickle.load(f)

    @property
    def countries(self):
        '''Property to list countries and codes.
        '''
        pprint.pprint(self.codes)
