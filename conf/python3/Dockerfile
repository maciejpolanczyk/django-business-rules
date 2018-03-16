FROM python:3.6

# Wheel install (needed for proper installing some other libraries), pip upgrade
RUN pip3 install --upgrade pip wheel

# Install requirements
ADD dbr/requirements-django2.0.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD dbr/requirements-development.txt requirements-development.txt
RUN pip3 install -r requirements-development.txt

WORKDIR /usr/src/app

# Add sources
ADD . /usr/src/app

WORKDIR /usr/src/app/dbr

# Create DB
RUN python3 manage.py migrate --traceback

# Start entry point
CMD ["echo dbr on python 3"]
