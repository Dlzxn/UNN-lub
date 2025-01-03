from bs4 import BeautifulSoup
import json

class AnalyticHtml:
    def __init__(self):
        self.load()
        # self.__inizial_soup()


    def load(self):
        with open('../bd/rasp.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            print(self.data)



a = AnalyticHtml()