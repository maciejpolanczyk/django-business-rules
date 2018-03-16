FROM python:2.7

# Wheel install (needed for proper installing some other libraries), pip upgrade
RUN pip install --upgrade pip wheel

# Install requirements
ADD dbr/requirements-django1.11.txt requirements.txt
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
