from __future__ import unicode_literals

from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from django_business_rules.models import BusinessRuleModel


class BusinessRuleListView(ListView):
    model = BusinessRuleModel
    context_object_name = 'business_rule_list'
    template_name = 'django_business_rules/business_rule_list.html'


class BusinessRuleFormView(UpdateView):
    model = BusinessRuleModel
    fields = ('rules', )
    template_name = 'django_business_rules/business_rule_form.html'
