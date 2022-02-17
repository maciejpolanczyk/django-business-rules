from __future__ import unicode_literals

from business_rules.actions import BaseActions
from business_rules.variables import BaseVariables

from django_business_rules.business_rule import BusinessRule


class ProductVariables(BaseVariables):
    def __init__(self, product):
        self.product = product


class ProductActions(BaseActions):
    def __init__(self, product):
        self.product = product


class ProductBusinessRule(BusinessRule):
    name = "django_business_rules.tests.product_business_rule.ProductBusinessRule"
    variables = ProductVariables
    actions = ProductActions


class ProductBusinessRuleToTestUpdate(BusinessRule):
    name = "django_business_rules.tests.product_business_rule.ProductBusinessRule"
    description = "updated ProductBusinessRule"
    variables = ProductVariables
    actions = ProductActions
