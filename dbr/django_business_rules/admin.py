from __future__ import unicode_literals

from django.contrib import admin

from django_business_rules.models import BusinessRuleModel


@admin.register(BusinessRuleModel)
class BusinessRuleAdmin(admin.ModelAdmin):
    pass
