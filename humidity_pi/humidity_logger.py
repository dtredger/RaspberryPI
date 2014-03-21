import os
import time
import datetime

DHT_BINARY = "./DHT_binary"

def read_humidity():
	try:
		# check_output(compiled binary location, sensor type, Arduino GPIO port)
		live_data = subprocess.check_output([DHT_BINARY, "2302", "4"])

		temp_group = re.search("Temp =\s+([0-9.]+)", live_data)
		if not temp_group:
			time.sleep(3)
			continue
		temp = float(temp_group.group(1))
		
		humidity_group = re.search("Hum =\s+([0-9.]+)", live_data)
		if not humidity_group:
			time.sleep(3)
			continue
		humidity = float(humidity_group.group(1))

		sensor_data = "T %s, H %s" % (temp, humidity)
	except:
		sensor_data = "could not read line.\n"
	return sensor_data

def log_output():
	timestamp = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y-%m-%d_%H.%M")
	filename = os.environ.get('HUMIDITY_LOG','hl_') + str(timestamp)
	try:
		with open(filename, 'w') as file:
			print "writing to %s" % filename
			while time.time() < ( time.time() + 86400):	  # one file per day
				file.write(str(int(time.time())) + ", " + read_humidity())
				file.flush()
				print read_humidity()
			file.close()
	except:
		print "couldn't write to %s" % filename
		print "exiting."
		raise SystemExit

while True:
	log_output()