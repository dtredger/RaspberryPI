# from http://docs.resin.io/#/pages/using/dockerfile.md


FROM resin/rpi-raspbian:wheezy-2015-01-15

# TORNADO WEBSERVER-PI
#Install python2 and pip
RUN apt-get update && apt-get install -yq --no-install-recommends \
		build-essential \
		python \
		python-dev \
		python-dbus \
		python-pip \
		sqlite3 \
	&& rm -rf /var/lib/apt/lists/*

#install python packages with pip
RUN pip install tornado

#set up supervisord to run multiple things
RUN pip install supervisor



#copy our python source into /app in the container
COPY . /app

#create database & table
RUN python /app/database_setup.py

#run main.py when the container starts
RUN supervisord -c /app/supervisord.conf

# CMD ["python", "/app/webserver_pi/tornado_pi/tornado_app.py"]






# https://github.com/waveform80/picamera
# RUN apt-get update && apt-get install -yq --no-install-recommends \
		# python-picamera \ 