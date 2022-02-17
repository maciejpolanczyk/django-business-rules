from __future__ import unicode_literals

from django.test import TestCase

try:
    # django < 1.10
    from django.core.urlresolvers import reverse
except ImportError:
    # django >= 1.10
    from django.urls import reverse

from django_business_rules.models import BusinessRuleModel
from django_business_rules.tests.product_business_rule import ProductBusinessRule


class BusinessRuleFormViewTests(TestCase):
    def test_should_place_rules_and_rule_data_in_hidden_inputs(self):
        # GIVEN
        rule = BusinessRuleModel.objects.create(
            name="test name",
            description="test description",
            rule_data="test rule data",
            rules='["test rules"]',
        )
        # WHEN
        response = self.client.get(
            reverse("django_business_rules:business-rule-form", kwargs={"pk": rule.pk})
        )
        # THEN
        self.assertEqual(response.status_code, 200, response.content)
        self.assertContains(
            response,
            '<input type="hidden" value=\'test rule data\' id="rule_data" name="rule_data" />',
        )
        self.assertContains(
            response,
            '<input type="hidden" value=\'[&quot;test rules&quot;]\' id="rules" name="rules" />',
        )

    def test_should_use_correct_template_to_render_business_rule_form(self):
        # GIVEN
        rule = BusinessRuleModel.objects.create(
            name="test name",
            description="test description",
            rule_data="test rule data",
            rules='["test rules"]',
        )
        # WHEN
        response = self.client.get(
            reverse("django_business_rules:business-rule-form", kwargs={"pk": rule.pk})
        )
        # THEN
        self.assertEqual(response.status_code, 200, response.content)
        self.assertTemplateUsed(
            response, "django_business_rules/business_rule_form.html"
        )

    def test_should_update_only_rule(self):
        # GIVEN
        rule = BusinessRuleModel.objects.create(
            name="test name",
            description="test description",
            rule_data="test rule data",
            rules='["test rules"]',
        )
        update_data = {
            "name": "updated name",
            "description": "updated description",
            "rule_data": "updated rule data",
            "rules": '{"key1": "value1"}',
        }
        # WHEN
        response = self.client.post(
            reverse("django_business_rules:business-rule-form", kwargs={"pk": rule.pk}),
            data=update_data,
        )
        # THEN
        self.assertEqual(response.status_code, 302, response.content)
        rule.refresh_from_db()
        self.assertEqual(rule.name, "test name")
        self.assertEqual(rule.description, "test description")
        self.assertEqual(rule.rule_data, "test rule data")
        self.assertEqual(rule.rules, '{"key1": "value1"}')

    def test_updated_rule_should_be_transfered_to_correct_object(self):
        # GIVEN
        rule = BusinessRuleModel.objects.create(
            name=ProductBusinessRule.name,
            description="test description",
            rule_data="test rule data",
            rules='["test rules"]',
        )
        update_data = {
            "rules": '{"key1": "value1"}',
        }
        # WHEN
        response = self.client.post(
            reverse("django_business_rules:business-rule-form", kwargs={"pk": rule.pk}),
            data=update_data,
        )
        # THEN
        self.assertEqual(response.status_code, 302, response.content)
        self.assertEqual(ProductBusinessRule.get_rules(), {"key1": "value1"})
