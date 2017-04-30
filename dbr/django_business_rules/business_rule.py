from __future__ import unicode_literals

import json

from business_rules import engine, utils

from django_business_rules.models import BusinessRuleModel


class BusinessRule(object):
    name = None
    description = ''
    variables = None
    actions = None

    @classmethod
    def generate(cls):
        cls._validate_rule_data()
        BusinessRuleModel.objects.update_or_create(
            name=cls.get_name(),
            defaults=cls._get_update_values(),
        )

    @classmethod
    def _validate_rule_data(cls):
        assert cls.variables is not None
        assert cls.actions is not None

    @classmethod
    def _get_update_values(cls):
        update_values = {
            'rule_data': cls._get_rule_data(),
        }
        if cls.description:
            update_values['description'] = cls.description
        return update_values

    @classmethod
    def _get_rule_data(cls):
        rule_data = utils.export_rule_data(cls.variables, cls.actions)
        return json.dumps(rule_data)

    @classmethod
    def run_all(cls, obj, stop_on_first_trigger=True):
        return engine.run_all(
            rule_list=cls.get_rules(),
            defined_variables=cls._get_variables_instance(obj),
            defined_actions=cls._get_actions_instance(obj),
            stop_on_first_trigger=stop_on_first_trigger
        )

    @classmethod
    def _get_variables_instance(cls, obj):
        return cls.variables(obj)

    @classmethod
    def _get_actions_instance(cls, obj):
        return cls.actions(obj)

    @classmethod
    def save_rules(cls, rules):
        rules_json = json.dumps(rules)
        BusinessRuleModel.objects.filter(name=cls.get_name()).update(rules=rules_json)

    @classmethod
    def get_rules(cls):
        return cls._get_object_from_json(
            BusinessRuleModel.objects.get(name=cls.get_name()).rules
        )

    @classmethod
    def get_rule_data(cls):
        return cls._get_object_from_json(
            BusinessRuleModel.objects.get(name=cls.get_name()).rule_data
        )

    @classmethod
    def get_name(cls):
        return cls.name if cls.name else cls._get_default_name()

    @classmethod
    def _get_default_name(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)

    @classmethod
    def _get_object_from_json(cls, text):
        return json.loads(text)
