RaspberryPI
===========

The Raspberry Pi is running Moebius v1.1.1, a small linux distro
http://moebiuslinux.sourceforge.net

There are three separate applications included in this repository:

####1) webserver_pi: (Tornado or Flask)

* Tornado Server (Python)
Using Tornado webserver (and tornado templates) because they're fast/minimalistic, and they're used some places at work. This is what's being actively used.

* Flask (Python)
Simple: My SD card was full, so couldn't install Django. Flask isn't being used going forward, but should still work.

####2) Humidity Logger

* The temp/humidity logger relies on *DHT_binary* to read a DHT-22 sensor attached to the Raspberry Pi's GPIO pins. *DHT_binary* is the compiled version of the DHT_binary.c file from Adafruit (included for reference). 
* Python code writes the sensor data to a csv one line at a time, updated whenever the sensor is (every 2 seconds). It creates a new timestamped csv file once per day. The location of the file is dependent on the HUMIDITY_LOG environment variable. Currently it's being saved to an external HD. 

####3) FM Radio

* Uses the *pifm* binary to transmit .wav audio over FM radio using the Rasperry Pi's GPIO pins.
* Python code creates playlists from folders of music, can set shuffle or continuous play. For files that are not in .wav format, it uses ffmpeg to convert, and streams this file (which is in fact written to dev/null!). The broadcast is currently set to 101.1 FM, but can only be heard a few meters away.


===========
There are Enviro variables so the two apps will run locally (for testing) and on the PI
* SERVER_PORT is 80 on the PI, but can't be that on yer macbook, so let's make it 8080
* DEBUG seems like it should be False for the PI, so that's set also.
* HUMIDITY_LOG is where the csv files written by the humidity logger go. It falls back to the current directory.

===========
###Dependencies
Are numerous in amount. A non-exhaustive list of them is:
* ffmpeg
* nginx