import base64
import json
import os
import re
import sys
import unittest
sys.path.append('../store_scrape/app_data')
from get_app_data import *


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_popular_apps(self):
        dats = ScrapetheStore("https://itunes.apple.com/us/genre/ios-weather/id6001?mt=8", country="Australia")
        print(dats.urlstart)
        dats.get_pop_apps(top=5)

if __name__ == "__main__":
    unittest.main()