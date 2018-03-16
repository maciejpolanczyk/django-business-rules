from __future__ import unicode_literals

from django.conf.urls import url

from django_business_rules.views import BusinessRuleFormView, BusinessRuleListView


app_name = 'django_business_rules'
urlpatterns = [
    url(r'^business-rule/$', BusinessRuleListView.as_view(), name='business-rule-list'),
    url(r'^business-rule/(?P<pk>[0-9]+)/$', BusinessRuleFormView.as_view(), name='business-rule-form'),
]
