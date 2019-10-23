import bs4 as bs
import os, sys
testdir = os.path.dirname(__file__)
srcdir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import requests
from store_data.appstore_info import GetStoreInfo
from store_data.appstore_content import GetAppContent
from store_data.store_codes import CountryCodes


class ScrapetheStore(GetStoreInfo, GetAppContent, CountryCodes):
    '''Class for scraping app information from the ios app store.
    GetAppInfo to get app info from the store -> driver for app id's/lists to obtain
    GetAppContent -> get app description, art etc, items present in the app store.
    UserReviews -> get reviews

    :param urlstart: Staring url for data.
    :type urlstart: str
    '''

    def __init__(self, urlstart=False, genre=False, country="United States"):
        super(ScrapetheStore, self).__init__(urlstart)
        self.get_genres()
        self.genre = genre
        self.urlstart = urlstart
        self.country = country
        self.country_codes = CountryCodes()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

    def self_check(self):
        if not self.urlstart:
            if not self.genre:
                while self.genre not in self.genres:
                    self.genre = input(f'Please enter a genre or starting URL {self.genres}')
            elif self.genre not in self.genres:
                while self.genre not in self.genres:
                    self.genre = input(f'Please enter a genre or starting URL {self.genres}')
            self.urlstart = self.genres[self.genre]

    @staticmethod
    def get_id(app_url):
        ''' Simple static method to return appid.

        :param app_url: appstore url for a specific app.
        :type app_url: str
        '''
        return app_url.split('id')[-1].split('?')[0]
        
    def get_top_apps(self, **kwargs):
        '''Method to obtain popular listed apps.
        '''
        top = kwargs.get('top', False)
        self.self_check()
        self.get_popular_apps()
        for title in self.popular_titles[:top if top else len(self.popular_titles)]:
            appid = self.get_id(title)
            print(appid)
            # content = GetAppContent()
            # reviews = UserReviews(appid, country=self.country)
            self.get_images_json(self.genre, [title,])
            # reviews.get_all_reviews()

    def get_all_apps(self):
        '''Works through the alpha list, gets pages/letter and retrieves app info.
        '''
        self.self_check()
        self.get_alpha_lists()
        for link in set(self.alpha):
            self.get_page_list(link)
            for lin in set(self.pages):
                res = requests.get(lin, headers=self.headers)
                res.raise_for_status()
                noStarchSoup = bs.BeautifulSoup(res.text, "lxml")

                for url in noStarchSoup.find_all('div', {"class":"grid3-column"}):
                    self.get_images_json(self.genre, [ul.get('href') for ul in url.find_all('a')])

def main():
    dats = ScrapetheStore("https://itunes.apple.com/us/genre/ios-weather/id6001?mt=8", country="United States")
    print(dats.urlstart)
    dats.get_top_apps()
if __name__ == "__main__":
    main()