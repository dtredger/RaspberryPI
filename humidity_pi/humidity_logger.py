import os
import sys
import time
import datetime
import subprocess
import re

DHT_BINARY = "./DHT_binary"
SENSOR_DELAY = 3
HUMIDITY_LOGS_LOCATION = os.environ.get("HUMIDITY_LOG_LOCATION","/500gb_hd/humidity_logs") + "/"
FILE_DURATION = 43200  #two files per day --> 60*60*24 / 2    ie (1/ 12 hrs)

def read_humidity():
	try:
		# check_output(compiled binary location, sensor type, Arduino GPIO port)
		live_data = subprocess.check_output([DHT_BINARY, "22", "17"])
		print live_data
		temp_group = re.search("Temp =\s+([0-9.]+)", live_data)
		temp = float(temp_group.group(1))
		
		humidity_group = re.search("Hum =\s+([0-9.]+)", live_data)
		humidity = float(humidity_group.group(1))

		sensor_data = "T %s, H %s\n" % (temp, humidity)
	except:
		print "could not read line."
		sensor_data = ""
	return sensor_data

def log_output(FILE_DURATION):
	timestamp = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y-%m-%d_%H.%M")
	filename = HUMIDITY_LOGS_LOCATION + "humidity_log_" + str(timestamp) + ".csv"
	try:
		with open(filename, 'w') as file:
			print "writing to %s" % filename
			while time.time() < ( time.time() + FILE_DURATION):
				sensor_reading = read_humidity()
				if sensor_reading:
					print sensor_reading
					file.write(str(int(time.time())) + ", " + sensor_reading)
					file.flush()
					print sensor_reading
				time.sleep(SENSOR_DELAY)
			file.close()
	except:
		print "couldn't write to %s" % filename
		print "exiting."
		raise SystemExit


# if this module is called directly, start executing
if __name__ == "__main__":
	try:
		if len(sys.argv) == 2:
			FILE_DURATION = sys.argv[1]
		log_output(FILE_DURATION)
	except KeyboardInterrupt:
		pass