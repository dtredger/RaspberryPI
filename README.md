RaspberryPI
===========

For a site hosted on Raspberry Pi

There are two separate apps set up:

* Tornado (Python)
Using Tornado webserver (and tornado templates) because they're fast/minimalistic, and they're used some places at work (gotta learn em)

* Flask (Python)
Simple: My SD card is full, so couldn't install Django.


There are Enviro variables so the two apps will run locally (for testing) and on the PI
* SERVER_PORT is 80 on the PI, but can't be that on yer macbook, so let's make it 8080
* DEBUG seems like it should be False for the PI, so that's set also.