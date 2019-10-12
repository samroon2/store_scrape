import unittest
import json
import base64
import re
import sys
import os
sys.path.append('../store_scrape/store_data')
from appstore_content import *


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'
app = 'https://apps.apple.com/us/app/sweatcoin/id971023427'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_sel_json(self):
        health_app = GetAppContent()
        health_app.get_selected_apps_json(category, [app])
        appid = re.findall(r'\d+', app)[0]
        with open(f"./{category}/{appid}.json") as f:
            apd = json.load(f)
        assert len(apd) != 0
        assert 'app_summary' in apd.keys()
        assert 'description' in apd['results'].keys()
        [os.remove(f"./{category}/{x}") for x in os.listdir(f"./{category}")]
        os.rmdir(f"./{category}")


if __name__ == "__main__":
    unittest.main()