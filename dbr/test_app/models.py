from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Products(models.Model):
    related_products = models.ManyToManyField('Products')
    current_inventory = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    @property
    def orders(self):
        return list(self.productorder_set.all())

    @staticmethod
    def top_holiday_items():
        return Products.objects.all()

    def __str__(self):
        return '{} {}'.format(self.price, self.current_inventory)

@python_2_unicode_compatible
class ProductOrder(models.Model):
    expiration_date = models.DateField()
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Products)

    def __str__(self):
        return '{} {} {}'.format(self.product, self.quantity, self.expiration_date)
