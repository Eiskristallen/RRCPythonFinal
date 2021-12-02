# import necessary libraries
from html.parser import HTMLParser
import urllib.request

# make WeatherScraper class


class WeatherScraper(HTMLParser):
    isTr = False
    isA = False
    isTd = False
    td_count = 0
    weather = {}
    days = -1
    year = 2018
    month = 1
    # year_month = 0;
    if month < 10:
        year_month = str(year)+'-'+'0'+str(month)
    else:
        year_month = str(year)+'-'+str(month)

    def parse_data(self):
        with urllib.request.urlopen('http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=1') as response:
            html = str(response.read())
        self.weather[str(self.year_month)] = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if bool(tag == 'tr'):
            self.isTr = True
            self.days = self.days + 1
        # if tag == 'a':
        #     self.isA = True
        if bool(tag == 'td') & bool(self.td_count <= 2):
            self.isTd = True
            self.td_count = self.td_count + 1

    def handle_endtag(self, tag):
        if bool(tag == 'tr'):
            self.isTr = False
            self.td_count = 0
            # print('\n')
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
        if self.isTr & self.isTd & bool('LegendE' not in data) & bool('LegendM' not in data):
            data = data.replace(r'\n', '').replace(
                r'\r', '').replace(r'\t', '')
            if 'M' in data:
                self.isTr = False
                return
            if 'E' in data:
                self.isTr = False
                return
        if self.isTr & self.isTd & bool('LegendE' not in data) & bool('LegendM' not in data):
            data = data.replace(r'\n', '').replace(
                r'\r', '').replace(r'\t', '')
            if self.td_count == 1:
                self.weather[self.year_month][str(self.days)
                                              ] = {'Max': float(data)}
            if self.td_count == 2:
                self.weather[self.year_month][str(self.days)
                                              ]['Min'] = float(data)
            if self.td_count == 3:
                self.weather[self.year_month][str(self.days)
                                              ]['Mean'] = float(data)


myparser = WeatherScraper()
myparser.parse_data()
print(myparser.weather)
