from __future__ import unicode_literals

from django.test import TestCase

try:
    # django < 1.10
    from django.core.urlresolvers import reverse
except ImportError:
    # django >= 1.10
    from django.urls import reverse


class BusinessRuleListViewTests(TestCase):
    def test_should_use_correct_template_to_render_business_rule_list(self):
        # GIVEN
        # WHEN
        response = self.client.get(reverse("django_business_rules:business-rule-list"))
        # THEN
        self.assertEqual(response.status_code, 200, response.content)
        self.assertTemplateUsed(
            response, "django_business_rules/business_rule_list.html"
        )
