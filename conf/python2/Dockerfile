FROM ubuntu:14.04

MAINTAINER Maciej Polanczyk  <maciej.polanczyk@stxnext.pl>

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install libs
RUN apt-get update && apt-get install -y \
    python-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists; rm -rf /tmp/*; \
    apt-get autoremove -y

# Wheel install (needed for proper installing some other libraries), pip upgrade
RUN pip install --upgrade pip wheel

# Install requirements
ADD dbr/requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD dbr/requirements-development.txt requirements-development.txt
RUN pip install -r requirements-development.txt

WORKDIR /usr/src/app

# Add sources
ADD . /usr/src/app

WORKDIR /usr/src/app/dbr

# Create DB
RUN python manage.py migrate --traceback

# Start entry point
CMD ["echo dbr on python 2.7"]
