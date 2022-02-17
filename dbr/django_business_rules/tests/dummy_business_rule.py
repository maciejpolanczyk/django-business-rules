from __future__ import unicode_literals

from django_business_rules.business_rule import BusinessRule


class DummyBusinessRule(BusinessRule):
    pass


class DummyBusinessRuleWithName(BusinessRule):
    name = "test_name"


class DummyBusinessRuleWithVariables(BusinessRule):
    variables = "test"


class DummyBusinessRuleWithVariablesAndActions(BusinessRule):
    variables = "test"
    actions = "test"
