from importlib import import_module

from django.apps import AppConfig
from django.apps import apps as django_apps
from django.conf import settings


class DbgettextConfig(AppConfig):
	name = 'dbgettext'
	
	def ready(self):
		REGISTRATION_MODULE_NAME = getattr(settings, 'DBGETTEXT_REGISTRATION_MODULE_NAME', 'dbgettext_registration')
		if hasattr(settings, 'DBGETTEXT_PROJECT_OPTIONS'):
			import_module(settings.DBGETTEXT_PROJECT_OPTIONS)
		for ac in django_apps.get_app_configs():
			try:
				import_module("%s.%s" % (ac.name, REGISTRATION_MODULE_NAME))
			except ImportError:
				continue
