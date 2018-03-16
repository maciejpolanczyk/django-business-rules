import inspect
import pkgutil

from django.conf import settings
from django.core.management.base import BaseCommand

from django_business_rules.business_rule import BusinessRule
from django_business_rules.models import BusinessRuleModel


class BusinessRuleGenerateException(Exception):
    pass


class Command(BaseCommand):
    help = 'Updates rules data in database'
    BUSINESS_RULE_MODULE_NAME = 'rules'

    def handle(self, *args, **options):
        self.stdout.write('This command will override all rules data in database.')
        business_rule_classes = self._find_business_rule_classes(options)
        self._validate(business_rule_classes, options)
        self._save(business_rule_classes, options)
        self.stdout.write('Done with SUCCESS.')

    def _find_business_rule_classes(self, options):
        result = []
        root_path = settings.BASE_DIR
        self._debug('Looking for business rules in: {} ...'.format(root_path), options)
        for module_loader, module_name, is_pkg in pkgutil.walk_packages([root_path]):
            if self._is_business_rule_module(module_loader, module_name, is_pkg, root_path):
                module = module_loader.find_module(module_name).load_module(module_name)
                result.extend(self._get_business_rule_classes(module))
        self._debug('Found business rules: {}'.format(result), options)
        return result

    @classmethod
    def _is_business_rule_module(cls, module_loader, module_name, is_pkg, root_path):
        return module_loader.path.startswith(root_path) \
               and not is_pkg \
               and module_name.endswith(Command.BUSINESS_RULE_MODULE_NAME)

    def _get_business_rule_classes(self, module):
        result = []
        for _, obj in inspect.getmembers(module):
            if self._is_business_rule_class(obj):
                result.append(obj)
        return result

    @classmethod
    def _is_business_rule_class(cls, obj):
        return inspect.isclass(obj) and issubclass(obj, BusinessRule) and obj is not BusinessRule

    def _validate(self, business_rule_classes, options):
        self._debug('Validating business rules...', options)
        unique_rule_names = {}
        for rule_class in business_rule_classes:
            name = rule_class.get_name()
            if name in unique_rule_names:
                raise BusinessRuleGenerateException(
                    'Not unique names for classes: {} and {}'.format(
                        rule_class, unique_rule_names[name]
                    )
                )
            unique_rule_names[name] = rule_class

        self._debug('Vaidation done', options)

    def _save(self, business_rule_classes, options):
        self._debug('Deleting business rules', options)
        BusinessRuleModel.objects.all().delete()
        self._debug('Saving business rules...', options)
        for rule_class in business_rule_classes:
            self._debug('Generating: {}'.format(rule_class.get_name()), options)
            rule_class.generate()
        self._debug('Saving done.', options)

    def _debug(self, text, options):
        if options['verbosity'] > 1:
            self.stdout.write(text)
