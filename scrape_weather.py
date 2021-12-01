# import necessary libraries
from html.parser import HTMLParser
import urllib.request

# make WeatherScraper class


class WeatherScraper(HTMLParser):
    isTr = False
    isA = False
    isTd = False
    td_count = 0

    def handle_starttag(self, tag, attrs):
        if bool(tag == 'tr'):
            self.isTr = True
        # if tag == 'a':
        #     self.isA = True
        if bool(tag == 'td') & bool(self.td_count <= 2):
            self.isTd = True
            self.td_count = self.td_count + 1

    def handle_endtag(self, tag):
        if bool(tag == 'tr'):
            self.isTr = False
            self.td_count = 0
        if bool(tag == 'td'):
            self.isTd = False
        # if tag == 'a':
        #     self.isA = False

    def handle_data(self, data):
        if 'Sum' in data:
            self.isTr = False
        if 'Avg' in data:
            self.isTr = False
        if 'Xtrm' in data:
            self.isTr = False
        if self.isTr & self.isTd & bool('LegendE' not in data) & bool('LegendM' not in data) & bool('E' not in data):
            data = data.replace(r'\n', '').replace(
                r'\r', '').replace(r'\t', '')
            print(data)
            # if self.isA:
            #     print(data + 'wdasd')


myparser = WeatherScraper()

with urllib.request.urlopen('http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5') as response:
    html = str(response.read())
myparser.feed(html)
