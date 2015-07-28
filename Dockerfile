# from http://docs.resin.io/#/pages/using/dockerfile.md


FROM resin/rpi-raspbian:wheezy-2015-01-15

#Install python2 and pip
RUN apt-get update && apt-get install -yq --no-install-recommends \
		build-essential \
		python \
		python-dev \
		python-dbus \
		python-pip \
	&& rm -rf /var/lib/apt/lists/*

#install python packages with pip
RUN pip install tornado

#copy our python source into /app in the container
COPY . /app

#run main.py when the container starts

CMD ["python", "/app/webserver_pi/tornado_pi/tornado_app.py"]