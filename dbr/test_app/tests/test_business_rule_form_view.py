from __future__ import unicode_literals

from django.test import TestCase

try:
    # django < 1.10
    from django.core.urlresolvers import reverse
except ImportError:
    # django >= 1.10
    from django.urls import reverse

from test_app.rules import ProductBusinessRule


class BusinessRuleFormViewTests(TestCase):
    def test_should_use_correct_template_to_render_business_rule_form(self):
        # GIVEN
        ProductBusinessRule.generate()
        # WHEN
        response = self.client.post(
            # not the best idea to put '1'
            # but no other idea how to do it without using model
            reverse("django_business_rules:business-rule-form", kwargs={"pk": 1})
        )
        # THEN
        self.assertEqual(response.status_code, 200, response.content)
        self.assertTemplateUsed(
            response, "django_business_rules/business_rule_form.html"
        )

    def test_form_should_update_rule(self):
        # GIVEN
        ProductBusinessRule.generate()
        update_data = {"rules": '{"key1": "value1"}'}
        # WHEN
        response = self.client.post(
            reverse("django_business_rules:business-rule-form", kwargs={"pk": 1}),
            data=update_data,
        )
        # THEN
        self.assertEqual(response.status_code, 302, response.content)
        self.assertEqual(ProductBusinessRule.get_rules(), {"key1": "value1"})
