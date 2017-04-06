FROM ubuntu:14.04

MAINTAINER Maciej Polanczyk  <maciej.polanczyk@stxnext.pl>

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install libs
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists; rm -rf /tmp/*; \
    apt-get autoremove -y

# Wheel install (needed for proper installing some other libraries), pip upgrade
RUN pip3 install --upgrade pip wheel

# Install requirements
RUN pip3 install django

# Install plugin (used COPY instead of ADD because ADD unzips)
COPY build/dist/django-business-rules-1.0.tar.gz django-business-rules-1.0.tar.gz
RUN pip3 install django-business-rules-1.0.tar.gz

# Install requirements for tests
ADD dbr/requirements-development.txt requirements-development.txt
RUN pip3 install -r requirements-development.txt

# Add sources
WORKDIR /usr/src/app
RUN django-admin startproject example .
RUN python3 manage.py startapp test_app
ADD dbr/test_app/migrations /usr/src/app/test_app/migrations
RUN rm /usr/src/app/test_app/tests.py
ADD dbr/test_app/tests /usr/src/app/test_app/tests
ADD dbr/test_app/models.py /usr/src/app/test_app/models.py
ADD dbr/test_app/rules.py /usr/src/app/test_app/rules.py
RUN sed -i -e 's/INSTALLED_APPS = \[/INSTALLED_APPS = \[ "django_business_rules","test_app.apps.TestAppConfig",/g' /usr/src/app/example/settings.py
RUN sed -i -e 's/import url/import url, include/g' /usr/src/app/example/urls.py
RUN sed -i -e 's/]/url\(r"^dbr\/", include\("django_business_rules.urls", namespace="django_business_rules"\)\) ]/g' /usr/src/app/example/urls.py

# Create DB
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate --traceback

# Generate rules
RUN python3 manage.py dbr

# Start entry point
CMD ["echo dbr-e2e on python 3"]
