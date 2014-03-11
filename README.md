RaspberryPI
===========

There are three separate things set up:

####1) Web Server: (either Tornado or Flask -- they both do the same thing)

* Tornado Server (Python)
Using Tornado webserver (and tornado templates) because they're fast/minimalistic, and they're used some places at work (gotta learn em)

* Flask (Python)
Simple: My SD card is full, so couldn't install Django.

####2) Humidity Logger

* reads serial input from an arduino and puts it onto the connected external hd

####3) FM Radio

* plays music on the hd on FM. Currently set to 101.1.
* Converts mp3, m4a, etc, to wav so they can play, then immediately chucks the .wav version into dev/null


===========
There are Enviro variables so the two apps will run locally (for testing) and on the PI
* SERVER_PORT is 80 on the PI, but can't be that on yer macbook, so let's make it 8080
* DEBUG seems like it should be False for the PI, so that's set also.
