from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from test_app.models import Product
from test_app.rules import ProductBusinessRule


@receiver(post_save, sender=Product)
def execute_product_business_rules(sender, instance, **kwargs):
    ProductBusinessRule.run_all(instance)
