=====
Django Business Rules
=====

Django Business Rules is a simple Django app to support business rules.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_business_rules" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_business_rules',
    ]

2. Include the business rules URLconf in your project urls.py like this::

    re_path(r'^dbr/', include('django_business_rules.urls', namespace='django_business_rules'))

3. Run `python manage.py migrate` to create the dbr models.

4. Run `python manage.py dbr` to generate business rules

5. Visit http://127.0.0.1:8000/dbr/business-rule/ to participate in the dbr.
