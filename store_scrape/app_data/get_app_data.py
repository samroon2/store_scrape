import os, sys
testdir = os.path.dirname(__file__)
srcdir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

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

    def __init__(self, urlstart=False, country="Australia"):
        super(ScrapetheStore, self).__init__(urlstart)
        self.get_genres()
        self.urlstart = urlstart if urlstart else input(f'Please instanciate class with a starting URL {self.genres}')
        self.country = country
        self.country_codes = CountryCodes()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

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
        self.get_popular_apps()
        for title in self.popular_titles[:top if top else len(self.popular_titles)]:
            appid = self.get_id(title)
            # content = GetAppContent()
            # reviews = UserReviews(appid, country=self.country)
            self.get_images_json([title,])
            # reviews.get_all_reviews()

def main():
    dats = ScrapetheStore("https://itunes.apple.com/us/genre/ios-weather/id6001?mt=8", country="Australia")
    print(dats.urlstart)
    dats.get_top_apps()
if __name__ == "__main__":
    main()