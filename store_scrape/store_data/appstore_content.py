import bs4 as bs
import datetime
import json
import requests
import os
import time
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer


class GetAppContent:
    '''Class for extracting data for apps.
    '''

    def get_raw_app_json(self, appid: str):
        '''Retrieve app data.

        :param appid: ID of ios application.
        :type appid: str
        '''
        lookupurl = "https://itunes.apple.com/lookup?id={}".format(appid)
        resp = requests.get(lookupurl)
        data = resp.json()
        return data

    def get_images(self, picurl: str, dirr: str, indexx: int):
        '''Method for downloading app images.
        '''
        fn = dirr + '/' + str(f'{indexx}_') + picurl.split("/")[-1]
        r = requests.get(picurl, stream=True)
        f = open(fn, 'wb')
        for chunk in r.iter_content(chunk_size=512 * 1024):
            if chunk:
                f.write(chunk)

    def get_all_apps(self):
        '''Works through the alpha list, gets pages/letter and retrieves app info.
        '''
        for link in set(self.alpha):
            print(link)
            self.getpagelist(link)
            for lin in set(self.pages):
                print(lin)
                res = requests.get(lin, headers=self.headers)
                res.raise_for_status()
                noStarchSoup = bs.BeautifulSoup(res.text, "lxml")

                for url in noStarchSoup.find_all('div', {"class":"grid3-column"}):
                    [self.get_images_json(ul) for ul in url.find_all('a')]

    def get_selected_apps_json(self, category: str, selectedtitles: list):
        '''Get data for a given category/list of selcted apps.

        :param category: App store category to be collected.
        :type category: str
        :param selectedtitles: List of selected titles urls.
        :type selectedtitles: list
        '''
        if not os.path.exists(f'./{category}'):
            os.makedirs(f'./{category}')
        for app in selectedtitles:
            print(selectedtitles.index(app))
            appid = app.split('id')[-1].split('?')[0]
            print(appid)
            appjson = self.get_app_json(appid)
            with open(f'./{category}/{str(appid)}.json', "w") as outfile:
                json.dump(appjson, outfile)
            time.sleep(1)

    def get_images_json(self, selectedtitles: list):
        '''Method that retrieves images and json for apps.

        :param apps: List of app urls to get.
        :type apps: list
        '''
        for app in selectedtitles:
            print(selectedtitles.index(app))
            appid = app.split('id')[-1].split('?')[0]
            print(appid)
            os.makedirs(f'./{str(appid)}')
            os.makedirs(f'./{str(appid)}/screenshots')
            os.makedirs(f'./{str(appid)}/ipadScreenshot')
            os.makedirs(f'./{str(appid)}/artwork')
            appjson = self.get_raw_app_json(appid)
            print(appjson)
            [self.get_images(x, f'./{str(appid)}/screenshots', n) for n, x in enumerate(appjson['results'][0]['screenshotUrls'])]
            [self.get_images(x, f'./{str(appid)}/ipadScreenshot', n) for n, x in enumerate(appjson['results'][0]['ipadScreenshotUrls'])]
            self.get_images(appjson['results'][0]['artworkUrl512'], f'./{str(appid)}/artwork', 0)
            with open(f'./{str(appid)}/{str(appid)}.json', "w") as outfile:
                json.dump(appjson, outfile)
            time.sleep(1)

    def get_app_json(self, appid: str):
        '''Method for obtaining app details in json, takes appid which is apples app specific ID.

        :param appid: ID of app.
        :type appid: str
        :returns data: Formated json.
        '''
        try:
            data = self.get_raw_app_json(appid)
            data['results'] = data['results'][0]
            data['date_obtained'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['lookup_url'] = "https://itunes.apple.com/lookup?id={}".format(appid)
            data['app_id'] = data['results']['trackId']
            data['app_name'] = data['results']['trackName']
            data['app_summary'] = str(self.textsummary(data['results']['description'].replace(">","")))
            #self.storejson(data)
            return data
        except Exception as e:
            print(e, "failed on: ",)

    def textsummary(self, text: str):
        '''Method to provide a 2 sentence summary of the app description.

        :param text: Body of text describing app.
        :type text: str
        '''
        parser = PlaintextParser(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        concatsent = []
        for x in summarizer(parser.document, 3):
            concatsent.append(str(x))
        concatsent.pop(0)
        return ".".join(concatsent)