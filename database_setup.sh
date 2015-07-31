# database_setup.sh

sqlite3 /data/temperature_humidity.db <<EOS 
	create table temp_humidity(Id INTEGER PRIMARY KEY, date TEXT, temp REAL, humidity REAL);
EOS