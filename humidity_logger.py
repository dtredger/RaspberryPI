import os
import time
import datetime
import serial

try:
    ser = serial.Serial(os.environ.get('ARDUINO'), 9600)
except:
    print "Find where yer Arduino is connected, and set that to an ARDUINO environment variable"


def read_humidity():
    try:
        sensor = ser.readline()
    except:
        sensor = "could not read line\n"
    return sensor

def log_output():
    timestamp = datetime.datetime.utcnow().replace( second=0, microsecond=0).strftime("%Y.%m.%d-%H:%M")
    with open(os.environ.get('HUMID_LOG','hl_') + str(timestamp), 'w') as file:
        #one file per day
        while time.time() < ( time.time() + 86400):
            file.write(str(int(time.time())) + " - " + read_humidity())
            file.flush()
            time.sleep(2)
            print read_humidity()
        file.close()

while True:
    log_output()