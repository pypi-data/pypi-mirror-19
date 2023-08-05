FROM ubuntu:latest
MAINTAINER Hans Roh <hansroh@gmail.com>

RUN apt-get update

RUN apt-get install -y python2.7
RUN apt-get install -y python-pip
RUN apt-get install -y libpython2.7-dev

# RUN apt-get install -y python3
# RUN apt-get install -y python3-pip
# RUN apt-get install -y libpython3.5-dev

RUN apt-get -y autoremove

RUN pip install psycopg2
RUN pip install -v --no-cache-dir skitaid

EXPOSE 5000

# docker build -t hansroh/skitaid
# do configure and prepare apps
# docker commit --change='CMD ["/usr/local/bin/skitaid.py", "start"]' -c "EXPOSE 5000" 7c3 hansroh/skitaid
# docker run -d -p 5000:5000 --restart=always hansroh/skitaid
