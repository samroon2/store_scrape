import unittest
import json
import base64
import sys
import os.path
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
        print(health.popular_titles)
        assert len(health.popular_titles) != 0

    def test_alpha_list(self):
        health = GetStoreInfo(url)
        health.get_alpha_lists()
        print(health.alpha)
        assert len(health.alpha) != 0

    def test_get_sel_json(self):
        get_card = GetStoreContent()
        print(get_card.get_selected_apps_json(category, [card.populartitles[0]]))

if __name__ == "__main__":
    unittest.main()