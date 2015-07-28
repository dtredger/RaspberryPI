# from http://docs.resin.io/#/pages/using/dockerfile.md


FROM resin/rpi-raspbian:wheezy-2015-01-15

# Install Python.
RUN apt-get update && apt-get install -y python

# won-t work fer now
# RUN tar xvzf tornado-4.2.1.tar.gz
# RUN cd tornado-4.2.1
# RUN python setup.py build
# RUN sudo python setup.py install

# CMD ["python", "webserver_pi/tornado_pi/tornado_app.py"]