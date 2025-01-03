from bs4 import BeautifulSoup

class AnalyticHtml:
    def __init__(self, req):
        self.request = req
        self.__inizial_soup()

    def __inizial_soup(self):
        self.soup = BeautifulSoup(self.request, 'html.parser')
        self.__account_info()
        self.__ruz()

    def __account_info(self):
        self.name = self.soup.find('span', class_='user-name').text

    def __ruz(self):
        self.rasp = self.soup.find('span', class_='ng-star-inserted')
        print(self.rasp)

