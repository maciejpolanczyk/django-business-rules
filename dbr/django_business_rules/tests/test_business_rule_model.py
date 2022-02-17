from __future__ import unicode_literals

from django.db.utils import IntegrityError
from django.test import TestCase

from django_business_rules.models import BusinessRuleModel


class BusinessRuleModelTests(TestCase):
    def test_name_should_be_unique(self):
        # GIVEN
        expected_message = (
            "UNIQUE constraint failed: django_business_rules_businessrulemodel.name"
        )
        expected_name = "test name"
        BusinessRuleModel.objects.create(name=expected_name)
        # WHEN & THEN
        with self.assertRaisesMessage(IntegrityError, expected_message):
            BusinessRuleModel.objects.create(name=expected_name)

    def test_should_return_name_as_string_representation(self):
        expected_name = "test name"
        rule = BusinessRuleModel(name="test name")
        self.assertEqual(rule.name, expected_name)
