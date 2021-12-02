# import necessary libraries
from html.parser import HTMLParser
import urllib.request

# make WeatherScraper class


class WeatherScraper(HTMLParser):
    isTr = False
    isTd = False
    isTitle = False
    td_count = 0
    weather = {}
    # weather['2021-11'] = {}
    days = 1
    year = 2021
    month = 12
    month_word = ''
    year_month = 0
    month_check_list = {'1': 'January', '2': 'February', '3': 'March', '4': 'April',
                        '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
    # once the month not in the title doesn't match the month in link terminate loop and return result
    terminate_loop = False

    def parse_data(self):
        while self.terminate_loop == False:
            for x in range(0, 12):
                if self.terminate_loop:
                    self.weather = dict(
                        [(k, v) for k, v in self.weather.items() if len(v) > 0])
                    return self.weather
                with urllib.request.urlopen('http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year='+str(self.year)+'&Month=+'+str(self.month)) as response:
                    html = str(response.read())
                    if self.month < 10:
                        self.year_month = str(
                            self.year)+'-'+'0'+str(self.month)
                    else:
                        self.year_month = str(
                            self.year)+'-'+str(self.month)
                self.feed(html)
                # print('retrieving data from' +
                #       str(self.year)+'month:'+str(self.month) + 'month_word' + str(self.month_word))
                self.month = self.month - 1
                if self.month == 0:
                    self.month = 12

                self.days = 1
            self.year = self.year - 1
        self.weather = dict([(k, v)
                            for k, v in self.weather.items() if len(v) > 0])
        return self.weather

    def handle_starttag(self, tag, attrs):
        if bool(tag == 'h1'):
            self.isTitle = True
        if bool(tag == 'tr'):
            self.isTr = True
            if self.terminate_loop == False:
                self.weather[str(self.year_month)+'-'+str(self.days)] = {}
        if bool(tag == 'td') & bool(self.td_count <= 2):
            self.isTd = True
            self.td_count = self.td_count + 1

    def handle_endtag(self, tag):
        if bool(tag == 'h1'):
            self.isTitle = False
        if bool(tag == 'tr'):
            self.isTr = False
            self.td_count = 0
        if bool(tag == 'td'):
            self.isTd = False

    def handle_data(self, data):
        if self.isTitle:
            self.month_word = data.split(' ')[4]
            if bool(self.month_word == self.month_check_list[str(self.month)]) == False:
                self.terminate_loop = True
                return
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
            if '\xa0' in data:
                self.isTr = False
        if self.isTr & self.isTd & bool('LegendE' not in data) & bool('LegendM' not in data) & (self.terminate_loop == False):
            data = data.replace(r'\n', '').replace(
                r'\r', '').replace(r'\t', '')
            if self.td_count == 1:
                self.weather[str(self.year_month)+'-' +
                             str(self.days)]['Max'] = float(data)
            if self.td_count == 2:
                self.weather[str(self.year_month)+'-' +
                             str(self.days)]['Min'] = float(data)
            if self.td_count == 3:
                self.weather[str(self.year_month)+'-' +
                             str(self.days)]['Mean'] = float(data)
                self.days = self.days + 1


myparser = WeatherScraper()
print(myparser.parse_data())
