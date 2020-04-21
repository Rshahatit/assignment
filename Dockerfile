FROM python:3.7-stretch
# RUN apk add build-base
# RUN apk add py-configobj libusb py-pip python-dev gcc linux-headers uwsgi
# RUN apk add make

# Cache a layer of OS deps
RUN apt-get update && apt-get install -y gnupg2 curl

# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
# RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - 
# build essential is debian package. libpq is a debian -> google it
RUN apt-get update && apt-get install -y build-essential libpq-dev python-dev 
# RUN apt-get update && apt-get install -y python3.7 
RUN python3.7 -m pip install pip

RUN pip3 install uwsgi
# RUN apt-get install -y python3.7

RUN pip3 install asyncio
 
COPY ./requirements.txt /wikiracer/

COPY ./Makefile /wikiracer/

WORKDIR /wikiracer

RUN make python-dependencies 


COPY ./assignment /wikiracer/assignment

# WORKDIR /wikiracer/assignment
# CMD ["ls"]
CMD ["uwsgi", "/wikiracer/assignment/assignment/uwsgi.ini"]
