import sqlite3


class DBOperations:
    def initialize_db(self):
        try:
            open('temp_data.sqlite')
            print("Database already exists!")
        except IOError as e:
            if e.args[0] == 2:  # No such file or directory
                blank_db = sqlite3.connect('temp_data.sqlite')
                print("Blank database created")
            else:  # permission denied or something else?
                print(e.args)

        # try:
        # conn = sqlite3.connect("weather.sqlite")
        # print("Opened database successfully.")
        # except Exception as e:
        #     print("Error opening DB:", e)
myDbo = DBOperations()
myDbo.initialize_db()
