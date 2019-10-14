import base64
import json
import os
import re
import sys
import unittest
sys.path.append('../store_scrape/store_data')
from appstore_info import *


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_popular_apps_info(self):
        health = GetStoreInfo(url)
        health.get_popular_apps()
        assert len(health.popular_titles) != 0

    def test_get_genres(self):
        health = GetStoreInfo(url)
        health.get_genres()
        print(health.genres)
        assert len(health.genres) != 0        

    def test_alpha_list(self):
        health = GetStoreInfo(url)
        health.get_alpha_lists()
        assert len(health.alpha) != 0


if __name__ == "__main__":
    unittest.main()
