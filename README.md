Django Business Rules
==============

[![build-status-image]][travis]
[![pypi-version]][pypi]

# Overview
With this plugin django users (customers or administrators) can setup business rules with html forms. Default layout is similar to django admin panel and can be easily overridden.
Business rules engine is implemented with [business-rules][business-rules-lib]

# Requirements

* Python (2.7, 3.2, 3.3, 3.4, 3.5)
* Django (1.9, 1.10, 1.11, 2.0)

# Installation

Install using `pip`...

    pip install django-business-rules

Add `'django_business_rules'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'django_business_rules',
    )

# Example

Let's take a look at a quick example of using Business rules plugin.

## Setup
Startup up a new project like so...

    pip install django
    pip install django-business-rules
    django-admin.py startproject example .
    ./manage.py startapp test_app


Now edit the `example/urls.py` module in your project (django 2.x):

```python
from django.urls import include, paths, re_path

# Include the business rules URLconf
urlpatterns = [
    ...
    re_path(r'^dbr/', include('django_business_rules.urls', namespace='django_business_rules'))
]
```

Now edit the `example/urls.py` module in your project (django 1.x):

```python
from django.conf.urls import include, url

# Include the business rules URLconf
urlpatterns = [
    ...
    url(r'^dbr/', include('django_business_rules.urls', namespace='django_business_rules'))
]
```

Add the following to your `example/settings.py` module:

```python
INSTALLED_APPS = (
    ...  # Make sure to include the default installed apps here.
    'django_business_rules',
    'test_app.apps.TestAppConfig',
)
```

## Usage

Add models to your `test_app/model.py` module:

```python
from django.db import models

class Products(models.Model):
    related_products = models.ManyToManyField('Products')
    current_inventory = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    @property
    def orders(self):
        return list(self.productorder_set.all())

    @staticmethod
    def top_holiday_items():
        return Products.objects.all()


class ProductOrder(models.Model):
    expiration_date = models.DateField()
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
```

Add variables and actions to your `test_app/rules.py` module (more about variables and actions can be found [here][business-rules-lib]):

```python
import datetime

from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable, \
    string_rule_variable, select_rule_variable
from django.utils import timezone

from test_app.models import Products

from test_app.models import ProductOrder

from django_business_rules.business_rule import BusinessRule


class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

    @numeric_rule_variable(label='Days until expiration')
    def expiration_days(self):
        last_order = self.product.orders[-1]
        expiration_days = (last_order.expiration_date - datetime.date.today()).days
        return expiration_days

    @string_rule_variable()
    def current_month(self):
        return timezone.now().strftime("%B")

    @select_rule_variable(options=Products.top_holiday_items())
    def goes_well_with(self):
        return [] # self.product.related_products


class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(params={"sale_percentage": FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        self.product.price *= (1.0 - sale_percentage)
        self.product.save()

    @rule_action(params={"number_to_order": FIELD_NUMERIC})
    def order_more(self, number_to_order):
        ProductOrder.objects.create(product_id=self.product.id,
                                    quantity=number_to_order,
                                    expiration_date=timezone.now() + timezone.timedelta(weeks=4))


class ProductBusinessRule(BusinessRule):
    variables = ProductVariables
    actions = ProductActions
```

Create and execute migrations:

    ./manage.py makemigrations
    ./manage.py migrate

Generate business rules:

    ./manage.py dbr

That's it, we're done!

    ./manage.py runserver

You can now open the list of business rules in your browser at `http://127.0.0.1:8000/dbr/` and edit them.

[build-status-image]: https://travis-ci.org/maciejpolanczyk/django-business-rules.svg?branch=master
[travis]: https://travis-ci.org/maciejpolanczyk/django-business-rules?branch=master
[pypi-version]: https://pypip.in/version/django-business-rules/badge.svg
[pypi]: https://pypi.python.org/pypi/django-business-rules
[business-rules-lib]: https://github.com/venmo/business-rules
