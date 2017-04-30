from __future__ import unicode_literals

import json
import os

from django.core.management import call_command
from django.test.testcases import TestCase
from django.utils.six import StringIO

from django_business_rules.models import BusinessRuleModel
from test_app.rules import ProductBusinessRule
from test_app.tests.data.test_resource_provider import TestResourceProvider


class DbrCommandTests(TestCase):

    COMMAND_NAME = 'dbr'

    def test_should_save_rule_in_database(self):
        # GIVEN
        with self.assertRaises(BusinessRuleModel.DoesNotExist):
            ProductBusinessRule.get_rule_data()
        out = StringIO()
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out)
            # THEN
            self.assertEqual(
                self._get_rule_data(),
                ProductBusinessRule.get_rule_data()
            )
        except Exception:
            self._print_output(out)
            raise

    def _get_rule_data(self):
        return self._get_json_test_resource('rule_data.json')

    def _get_json_test_resource(self, file_name):
        with open(
                os.path.join(
                    TestResourceProvider.get_test_data_dir(),
                    file_name
                )
        ) as file_path:
            return json.load(file_path)

    @classmethod
    def _print_output(cls, out):
        out.seek(0)
        for line in out.readlines():
            print(line)
