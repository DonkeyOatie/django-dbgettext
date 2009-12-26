# based on django.contrib.admin.__init__.py

from django.utils.importlib import import_module
LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS dbgettext.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('gettext', app_path)
        except ImportError:
            continue

        import_module("%s.gettext" % app)

    LOADING = False

# go:
autodiscover()
