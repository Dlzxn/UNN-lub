from bs4 import BeautifulSoup

class AnalyticHtml:
    def __init__(self, req):
        self.request = req

    def __inizial(self):
        soup = BeautifulSoup(self.request, 'html.parser')
