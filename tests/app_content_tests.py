import base64
import json
import os
import re
import sys
import unittest
sys.path.append('../store_scrape/store_data')
from appstore_content import *


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'
app = 'https://apps.apple.com/us/app/sweatcoin/id971023427'
appid = re.findall(r'\d+', app)[0]

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_raw(self):
        ''' Test for getting raw json for a give app.
        '''
        health_app = GetAppContent()
        apd = health_app.get_raw_app_json(appid)
        assert len(apd) != 0
        assert 'results' in apd.keys()
        assert 'description' in apd['results'][0].keys()

    def test_get_images(self):
        health_app = GetAppContent()
        apd = health_app.get_raw_app_json(appid)
        img = apd['results'][0]['screenshotUrls'][0]
        health_app.get_images(img, './img', 1)
        assert len(os.listdir('./img')) != 0
        [os.remove(f"./img/{x}") for x in os.listdir(f"./img")]
        os.rmdir("./img")

    def test_get_sel_json(self):
        health_app = GetAppContent()
        health_app.get_selected_apps_json(category, [app])
        with open(f"./{category}/{appid}.json") as f:
            apd = json.load(f)
        assert len(apd) != 0
        assert 'app_summary' in apd.keys()
        assert 'description' in apd['results'].keys()
        [os.remove(f"./{category}/{x}") for x in os.listdir(f"./{category}")]
        os.rmdir(f"./{category}")


if __name__ == "__main__":
    unittest.main()