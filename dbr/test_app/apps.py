from __future__ import unicode_literals

from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = 'test_app'

    def ready(self):
        import test_app.signals  # noqa: F401 imported but unused
