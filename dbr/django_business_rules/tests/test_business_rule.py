from __future__ import unicode_literals

from mock import patch, Mock

from business_rules import engine
from django.test import TestCase

from django_business_rules.business_rule import BusinessRule
from django_business_rules.models import BusinessRuleModel
from django_business_rules.tests.dummy_business_rule import (
    DummyBusinessRule,
    DummyBusinessRuleWithName,
    DummyBusinessRuleWithVariables,
)
from django_business_rules.tests.product_business_rule import (
    ProductBusinessRule,
    ProductBusinessRuleToTestUpdate,
)


# TODO: use parameterized unit tests
class BusinessRuleTests(TestCase):
    def test_should_generate_name_from_base_BusinessRule_class_and_module(self):
        actual = BusinessRule.get_name()
        expected = "django_business_rules.business_rule.BusinessRule"
        self.assertEqual(actual, expected)

    def test_should_generate_name_from_DummyBusinessRule_class_and_module(self):
        actual = DummyBusinessRule.get_name()
        expected = "django_business_rules.tests.dummy_business_rule.DummyBusinessRule"
        self.assertEqual(actual, expected)

    def test_should_generate_name_from_name_field(self):
        actual = DummyBusinessRuleWithName.get_name()
        expected = "test_name"
        self.assertEqual(actual, expected)

    def test_should_raise_assertion_when_variables_missing(self):
        with self.assertRaises(AssertionError):
            DummyBusinessRule.generate()

    def test_should_raise_assertion_when_actions_missing(self):
        with self.assertRaises(AssertionError):
            DummyBusinessRuleWithVariables.generate()

    def test_should_create_rule_model_in_db(self):
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        self.assertTrue(BusinessRuleModel.objects.filter(name=expected_name).exists())

    def test_should_create_rule_model_in_db_with_empty_dict_as_rule(self):
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        expected_rules = "{}"
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).rules, expected_rules
        )

    def test_should_update_rule_model_in_db(self):
        # GIVEN
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).description, ""
        )
        # WHEN
        ProductBusinessRuleToTestUpdate.generate()
        # THEN
        expected_description = "updated ProductBusinessRule"
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).description,
            expected_description,
        )

    def test_update_should_not_change_rules_in_db(self):
        # GIVEN
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        ProductBusinessRule.save_rules({"key1": "value1"})
        expected_rules = '{"key1": "value1"}'
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).rules, expected_rules
        )
        # WHEN
        ProductBusinessRuleToTestUpdate.generate()
        # THEN
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).rules, expected_rules
        )

    def test_should_save_rules_in_db(self):
        # GIVEN
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        expected_rules = '{"key1": "value1"}'
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        # WHEN
        ProductBusinessRule.save_rules({"key1": "value1"})
        # THEN
        self.assertEqual(
            BusinessRuleModel.objects.get(name=expected_name).rules, expected_rules
        )

    def test_should_get_rules_from_db(self):
        # GIVEN
        expected_name = (
            "django_business_rules.tests.product_business_rule.ProductBusinessRule"
        )
        expected_rules = {"key1": "value1"}
        self.assertFalse(BusinessRuleModel.objects.filter(name=expected_name).exists())
        ProductBusinessRule.generate()
        ProductBusinessRule.save_rules({"key1": "value1"})
        # WHEN
        actual_rules = ProductBusinessRule.get_rules()
        # THEN
        self.assertEqual(actual_rules, expected_rules)

    @patch.object(ProductBusinessRule, "get_rules")
    @patch.object(ProductBusinessRule, "_get_variables_instance")
    @patch.object(ProductBusinessRule, "_get_actions_instance")
    @patch.object(engine, "run_all")
    def test_should_execute_run_all_with_correct_parameters(
        self,
        mock_for_run_all,
        mock_for_get_actions,
        mock_for_get_variables,
        mock_for_get_rules,
    ):
        # GIVEN
        mock_for_rules = Mock()
        mock_for_get_rules.return_value = mock_for_rules
        mock_for_variables = Mock()
        mock_for_get_variables.return_value = mock_for_variables
        mock_for_actions = Mock()
        mock_for_get_actions.return_value = mock_for_actions
        mock_for_product = Mock()
        # WHEN
        ProductBusinessRule.run_all(mock_for_product)
        # THEN
        mock_for_run_all.assert_called_once_with(
            rule_list=mock_for_rules,
            defined_variables=mock_for_variables,
            defined_actions=mock_for_actions,
            stop_on_first_trigger=True,
        )
