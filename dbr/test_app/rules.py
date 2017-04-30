from __future__ import unicode_literals

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
        return timezone.now().strftime('%B')

    @select_rule_variable(options=Products.top_holiday_items())
    def goes_well_with(self):
        return [] # self.product.related_products


class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(params={'sale_percentage': FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        self.product.price *= (1.0 - sale_percentage)
        self.product.save()

    @rule_action(params={'number_to_order': FIELD_NUMERIC})
    def order_more(self, number_to_order):
        ProductOrder.objects.create(product=self.product,
                                    quantity=number_to_order,
                                    expiration_date=timezone.now() + timezone.timedelta(weeks=4))


class ProductBusinessRule(BusinessRule):
    variables = ProductVariables
    actions = ProductActions
