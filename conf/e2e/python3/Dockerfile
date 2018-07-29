FROM python:3.7

# Wheel install (needed for proper installing some other libraries), pip upgrade
RUN pip install --upgrade pip wheel

# Install requirements
RUN pip install django

# Install plugin (used COPY instead of ADD because ADD unzips)
COPY build/dist/django-business-rules-*.tar.gz django-business-rules.tar.gz
RUN pip install django-business-rules.tar.gz

# Install requirements for tests
ADD dbr/requirements-development.txt requirements-development.txt
RUN pip install -r requirements-development.txt

# Add sources
WORKDIR /usr/src/app
RUN django-admin startproject example .
RUN python manage.py startapp test_app
ADD dbr/test_app/migrations /usr/src/app/test_app/migrations
RUN rm /usr/src/app/test_app/tests.py
ADD dbr/test_app/tests /usr/src/app/test_app/tests
ADD dbr/test_app/models.py /usr/src/app/test_app/models.py
ADD dbr/test_app/rules.py /usr/src/app/test_app/rules.py
RUN sed -i -e 's/INSTALLED_APPS = \[/INSTALLED_APPS = \[ "django_business_rules","test_app.apps.TestAppConfig",/g' /usr/src/app/example/settings.py
RUN sed -i -e 's/import path/import include, path, re_path/g' /usr/src/app/example/urls.py
RUN sed -i -e 's/]/re_path\(r"^dbr\/", include\("django_business_rules.urls", namespace="django_business_rules"\)\) ]/g' /usr/src/app/example/urls.py

# Create DB
RUN python manage.py makemigrations
RUN python manage.py migrate --traceback

# Generate rules
RUN python3 manage.py dbr

# Start entry point
CMD ["echo dbr-e2e on python 3"]
