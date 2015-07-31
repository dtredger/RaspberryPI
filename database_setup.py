import os
import sys
import sqlite3

LOG_TABLE_NAME = 'temp_humidity'
LOG_DATABASE_NAME = os.environ.get("LOG_DATABASE_NAME","temperature_humidity.db")


def create_table(database_name, table_name):
	conn = sqlite3.connect(database_name)
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE {0}(Id INTEGER PRIMARY KEY, date TEXT, temp REAL, humidity REAL)".format(table_name))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	create_table(LOG_DATABASE_NAME, LOG_TABLE_NAME)