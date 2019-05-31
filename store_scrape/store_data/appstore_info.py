import bs4 as bs
import requests


class GetStoreInfo:
    '''Class for obtaining lists of apps to etract relevant data for.

    :param urlstart: Starting url for scraping, should be a genre/category based url.
    :type urlstart: str
    :example urlstart: https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8
    '''

    def __init__(self, urlstart):
        self.urlstart = urlstart
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        self.popular_titles = []
        self.alpha = []
        self.pages = []
        self.all_pages = {}

    def get_popular_apps(self):
        '''Retrieves popular apps for a given category, approx 240 for each category.
        '''
        res = requests.get(self.urlstart, headers=self.headers)
        res.raise_for_status()
        noStarchSoup = bs.BeautifulSoup(res.text, 'lxml')
        for url in noStarchSoup.find_all('div', {'class': 'grid3-column'}):
            [self.popular_titles.append(ul.get('href')) for ul in url.find_all('a')]

    def get_alpha_lists(self):
        '''Scrapes the alphabet list present on the page and populates the alpha list.
        '''
        res = requests.get(self.urlstart, headers=self.headers)
        res.raise_for_status()
        noStarchSoup = bs.BeautifulSoup(res.text, 'lxml')

        for url in noStarchSoup.find_all('ul', {'class': 'list alpha'}):
            [self.alpha.append(ul.get('href')) for ul in url.find_all('a')]

    def get_page_list(self, alphurl):
        '''Method that scrapes the number of pages per letter and populates the pages list.
        '''
        res = requests.get(alphurl, headers=self.headers)
        res.raise_for_status()
        noStarchSoup = bs.BeautifulSoup(res.text, 'lxml')
        self.pages.clear()

        for url in noStarchSoup.find_all('ul', {'class': 'list paginate'}):
            [self.pages.append(ul.get('href')) for ul in url.find_all('a')]

    def get_all_alpha_pages(self):
        self.get_alpha_lists()
        self.all_pages = {x[-1]: [] for x in self.alpha}
        for letter in self.alpha:
            self.get_page_list(letter)
            for pages in self.pages:
                res = requests.get(self.urlstart, headers=self.headers)
                res.raise_for_status()
                noStarchSoup = bs.BeautifulSoup(res.text, 'lxml')
                for url in noStarchSoup.find_all('div', {'class': 'grid3-column'}):
                    [self.all_pages[letter[-1]].append(ul.get('href')) for ul in url.find_all('a')]         