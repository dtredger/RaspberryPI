import os
import time
import serial

try:
    ser = serial.Serial(os.environ.get('ARDUINO'), 9600)
except:
    print "Find where yer Arduino is connected, and set that to an ARDUINO environment variable"


def read_humidity():
    try:
        sensor = ser.readline()
    except:
        sensor = "not connected\n"
    return sensor

def log_output():
    timestamp = int(time.time())
    with open(os.environ.get('HUMID_LOG','humid_') + str(timestamp), 'w') as file:
        #one file per hour
        while int(time.time()) < (timestamp + 3600):
            file.write(read_humidity())
            file.flush()
            time.sleep(2)
            print read_humidity()
        file.close()

while True:
    log_output()