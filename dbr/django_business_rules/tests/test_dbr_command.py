from __future__ import unicode_literals

from mock import patch, MagicMock

from django.core.management import call_command
from django.test.testcases import TestCase
from django.utils import six

from django_business_rules.management.commands import dbr
from django_business_rules.management.commands.dbr import BusinessRuleGenerateException
from django_business_rules.models import BusinessRuleModel
from django_business_rules.tests.product_business_rule import ProductBusinessRule


class DbrCommandTests(TestCase):

    COMMAND_NAME = "dbr"

    @patch.object(dbr.Command, "_validate", MagicMock)
    @patch.object(dbr.Command, "_save", MagicMock)
    def test_should_find_BusinessRule_subclasses(self):
        # GIVEN
        out = six.StringIO()
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out)
            # THEN
            self.assertIn(
                "Found business rules: [<class 'test_app.rules.ProductBusinessRule'>]",
                out.getvalue(),
            )
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    @patch.object(dbr.Command, "_save", MagicMock)
    def test_should_raise_BusinessRuleGenerateException_when_names_not_unique(
        self, mock_for_find
    ):
        # GIVEN
        mock_for_find.return_value = [
            self._get_mock_for_business_class(name="test.business_rule_1"),
            self._get_mock_for_business_class(name="test.business_rule_1"),
        ]
        out = six.StringIO()
        expected_message = "Not unique names for classes: "
        try:
            # WHEN & THEN
            with self.assertRaisesMessage(
                BusinessRuleGenerateException, expected_message
            ):
                call_command(self.COMMAND_NAME, verbosity=2, stdout=out)
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    def test_should_call_generate_on_business_rule_subclasses(self, mock_for_find):
        # GIVEN
        mock_for_business_class = self._get_mock_for_business_class(
            name="test.business_rule_1"
        )
        mock_for_find.return_value = [mock_for_business_class]
        out = six.StringIO()
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out)
            # THEN
            mock_for_business_class.generate.assert_called_once()
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    def test_should_save_rule_in_database(self, mock_for_find):
        # GIVEN
        mock_for_find.return_value = [ProductBusinessRule]
        self.assertEqual(0, BusinessRuleModel.objects.count())
        out = six.StringIO()
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out)
            # THEN
            self.assertEqual(
                1,
                BusinessRuleModel.objects.filter(
                    name=ProductBusinessRule.get_name()
                ).count(),
            )
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    def test_should_remove_not_supported_rules(self, mock_for_find):
        # GIVEN
        mock_for_find.return_value = [ProductBusinessRule]
        self.assertEqual(0, BusinessRuleModel.objects.count())
        out = six.StringIO()
        BusinessRuleModel.objects.create(
            name="Not supported rule",
            description="",
            rule_data="",
        )
        try:
            # WHEN
            call_command(
                self.COMMAND_NAME,
                verbosity=2,
                stdout=out,
                interactive=False,
                remove=True,
            )
            # THEN
            self.assertEqual(1, BusinessRuleModel.objects.count())
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    def test_should_not_remove_not_supported_rules(self, mock_for_find):
        # GIVEN
        mock_for_find.return_value = [ProductBusinessRule]
        self.assertEqual(0, BusinessRuleModel.objects.count())
        out = six.StringIO()
        BusinessRuleModel.objects.create(
            name="Not supported rule",
            description="",
            rule_data="",
        )
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out, interactive=False)
            # THEN
            self.assertEqual(2, BusinessRuleModel.objects.count())
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    @patch.object(six, "input")
    def test_should_remove_not_supported_rules_in_interactive_mode(
        self, mock_for_input, mock_for_find
    ):
        # GIVEN
        mock_for_find.return_value = [ProductBusinessRule]
        self.assertEqual(0, BusinessRuleModel.objects.count())
        out = six.StringIO()
        mock_for_input.return_vale = "T"
        BusinessRuleModel.objects.create(
            name="Not supported rule",
            description="",
            rule_data="",
        )
        try:
            # WHEN
            call_command(
                self.COMMAND_NAME,
                verbosity=2,
                stdout=out,
                interactive=False,
                remove=True,
            )
            # THEN
            self.assertEqual(1, BusinessRuleModel.objects.count())
        except Exception:
            self._print_output(out)
            raise

    @patch.object(dbr.Command, "_find_business_rule_classes")
    @patch.object(six, "input")
    def test_should_not_remove_not_supported_rules_in_interactive_mode(
        self, mock_for_input, mock_for_find
    ):
        # GIVEN
        mock_for_find.return_value = [ProductBusinessRule]
        self.assertEqual(0, BusinessRuleModel.objects.count())
        out = six.StringIO()
        mock_for_input.return_vale = ""
        BusinessRuleModel.objects.create(
            name="Not supported rule",
            description="",
            rule_data="",
        )
        try:
            # WHEN
            call_command(self.COMMAND_NAME, verbosity=2, stdout=out, interactive=True)
            # THEN
            self.assertEqual(2, BusinessRuleModel.objects.count())
        except Exception:
            self._print_output(out)
            raise

    @classmethod
    def _get_mock_for_business_class(cls, name):
        mock_for_business_rule = MagicMock()
        mock_for_business_rule.get_name.return_value = name
        return mock_for_business_rule

    @classmethod
    def _print_output(cls, out):
        out.seek(0)
        for line in out.readlines():
            print(line)
