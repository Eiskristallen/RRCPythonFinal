import sqlite3
# from scrape_weather import WeatherScraper
# myparser = WeatherScraper()


class DBOperations:
    blanl_db = None
    db_cursor = None

    def initialize_db(self):
        try:
            open('temp_data.sqlite')
            print("Database already exists!")
            self.blank_db = sqlite3.connect('temp_data.sqlite')
            self.db_cursor = self.blank_db.cursor()
        except IOError as e:
            if e.args[0] == 2:
                self.blank_db = sqlite3.connect('temp_data.sqlite')
                try:
                    self.db_cursor = self.blank_db.cursor()
                    self.db_cursor.execute("""create table samples
                    (id integer primary key autoincrement not null,
                    sample_date text UNIQUE,
                    location text not null,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);""")
                    self.blank_db.commit()
                    print("Table created successfully.")
                except Exception as e:
                    print("Error creating table:", e)
                print("Blank database created")
            else:
                print(e.args)

    def save_data(self, data):
        """save temp data into database if it's not exsit

        Args:
            data (['simple_date:[simple_temp]']): data that going to store in db
            db_cursor cursor obj of the db
            db_connect connection obj with the db
        """
        temp_data = []
        for key, value in data.items():
            temp_data.append((key, str(data[key]['Max']), str(
                data[key]['Min']), str(data[key]['Mean']), 'Winnipeg, MB'))
        try:
            sql = """insert into samples (sample_date,max_temp,min_temp,avg_temp,location)
             values (?,?,?,?,?)"""
            for item in temp_data:
                self.db_cursor.execute(sql, item)
            self.blank_db.commit()
            print("Added data successfully.")
            self.blank_db.close()
        except Exception as e:
            print("Error inserting sample. Duplicate data detected")
            self.blank_db.close()

    def purge_data(self):
        try:
            self.db_cursor.execute("DELETE FROM samples")
            self.blank_db.commit()
            self.blank_db.close()
            print('delete data successfully')
        except Exception as e:
            print('An exception occurred', e)

    def fetch_data(self, start_date, end_date):
        try:
            sql = """select * from samples where date(sample_date) between '%s' and '%s'""" % (
                start_date, end_date)
            print(sql)
            return self.db_cursor.execute(sql)
        except Exception as e:
            print('An exception occurred', e)


myDbo = DBOperations()
myDbo.initialize_db()
print(myDbo.fetch_data("2000-11-02", "2001-10-01"))
# print(myDbo.save_data(myparser.parse_data()))
# myDbo.purge_data()
