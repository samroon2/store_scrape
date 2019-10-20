import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../store_scrape/app_data')
from get_app_data import *
from unittest.mock import patch


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_popular_apps(self):
        '''Test to get popular apps.
        '''
        dats = ScrapetheStore(urlstart=url, country="United States")
        print(dats.urlstart)
        dats.get_top_apps(top=5)
        downloads = [x for x in os.listdir('.') if '.py' not in x]
        assert len(downloads) > 0
        [shutil.rmtree(f"./{x}") for x in downloads]

if __name__ == "__main__":
    unittest.main()