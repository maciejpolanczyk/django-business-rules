from __future__ import unicode_literals

import json
import os

import datetime
from business_rules.engine import run_all
from business_rules.utils import export_rule_data
from django.test import TestCase
from django.utils import timezone
from mock import patch, Mock
from model_mommy import mommy

from test_app.rules import ProductVariables, ProductActions
from test_app.models import Products, ProductOrder
from test_app.tests.data.test_resource_provider import TestResourceProvider


# TODO: parameterized unit tests
class BusinessRulesLibraryTests(TestCase):
    maxDiff = None

    def test_should_export_product_rule_data(self):
        actual = export_rule_data(ProductVariables, ProductActions)
        expected = self._get_rule_data()
        self.assertEqual(actual, expected)

    def test_should_execute_rules_1(self):
        # GIVEN
        product_for_sale = mommy.make(Products, current_inventory=21, price=200)
        product_not_for_sale_1 = mommy.make(Products, current_inventory=20, price=200)
        product_not_for_sale_2 = mommy.make(Products, current_inventory=21, price=200)

        product_orders_for_sale = mommy.make(
            ProductOrder,
            product=product_for_sale,
            expiration_date=timezone.now()+timezone.timedelta(days=4)
        )
        product_orders_not_for_sale_1 = mommy.make(
            ProductOrder,
            product=product_not_for_sale_1,
            expiration_date=timezone.now() + timezone.timedelta(days=4)
        )
        product_orders_not_for_sale_2 = mommy.make(
            ProductOrder,
            product=product_not_for_sale_2,
            expiration_date=timezone.now() + timezone.timedelta(days=5)
        )

        rules = self._get_rules()
        # WHEN
        for product in Products.objects.all():
            run_all(
                rule_list=rules,
                defined_variables=ProductVariables(product),
                defined_actions=ProductActions(product),
                stop_on_first_trigger=True
            )
        # THEN
        product_for_sale.refresh_from_db()
        product_not_for_sale_1.refresh_from_db()
        product_not_for_sale_2.refresh_from_db()
        self.assertEqual(product_for_sale.price, 150)
        self.assertEqual(product_not_for_sale_1.price, 200)
        self.assertEqual(product_not_for_sale_2.price, 200)

    @patch.object(
        timezone,
        'now',
        Mock(return_value=datetime.datetime(2015, 6, 1, tzinfo=timezone.utc))
    )
    def test_should_execute_rules_2(self):
        # GIVEN
        product_for_order = mommy.make(Products, current_inventory=4, price=200)
        product_not_for_order = mommy.make(Products, current_inventory=5, price=200)
        # WHEN & THEN
        self._assert_rule_executed(product_for_order, product_not_for_order)

    @patch.object(
        timezone,
        'now',
        Mock(return_value=datetime.datetime(2015, 12, 1, tzinfo=timezone.utc))
    )
    def test_should_execute_rules_3(self):
        # GIVEN
        product_for_order = mommy.make(Products, current_inventory=19, price=200)
        product_not_for_order = mommy.make(Products, current_inventory=20, price=200)
        # WHEN & THEN
        self._assert_rule_executed(product_for_order, product_not_for_order)

    def _assert_rule_executed(self, product_for_order, product_not_for_order):
        # GIVEN
        product_orders_for_order = mommy.make(
            ProductOrder,
            product=product_for_order,
            expiration_date=datetime.datetime.now() + timezone.timedelta(days=4)
        )
        product_orders_not_for_order = mommy.make(
            ProductOrder,
            product=product_not_for_order,
            expiration_date=datetime.datetime.now() + timezone.timedelta(days=4)
        )

        self.assertFalse(
            ProductOrder.objects.filter(
                product=product_for_order,
                quantity=40
            ).exists()
        )
        self.assertFalse(
            ProductOrder.objects.filter(
                product=product_not_for_order,
                quantity=40
            ).exists()
        )

        rules = self._get_rules()
        # WHEN
        for product in Products.objects.all():
            run_all(
                rule_list=rules,
                defined_variables=ProductVariables(product),
                defined_actions=ProductActions(product),
                stop_on_first_trigger=True
            )
        # THEN
        self.assertTrue(
            ProductOrder.objects.filter(
                product=product_for_order,
                quantity=40
            ).exists()
        )
        self.assertFalse(
            ProductOrder.objects.filter(
                product=product_not_for_order,
                quantity=40
            ).exists()
        )

    def _get_rule_data(self):
        return self._get_json_test_resource('rule_data.json')

    def _get_rules(self):
        return self._get_json_test_resource('rules.json')

    def _get_json_test_resource(self, file_name):
        with open(
                os.path.join(
                    TestResourceProvider.get_test_data_dir(),
                    file_name
                )
        ) as file_path:
            return json.load(file_path)
