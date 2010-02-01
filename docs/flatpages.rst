.. _flatpages:

Example Usage: ``django.contrib.flatpages``
===========================================

Settings
--------
``settings.py``::

    DBGETTEXT_PROJECT_OPTIONS = 'my_project.dbgettext_options'

Registration
------------
``my_project/dbgettext_options.py``:

    from dbgettext.registry import registry, Options
    from dbgettext.lexicons import html
    from django.contrib.flatpages.models import FlatPage

    class FlatPageOptions(Options):
	attributes = ('title',)
	parsed_attributes = {'content': html.lexicon}

    registry.register(FlatPage, FlatPageOptions)


Template
--------
``templates/flatpages/default.html``::

    {% load dbgettext_tags i18n %}
    <html>
    <head>
    <title>{% trans flatpage.title %}</title>
    </head>
    <body>
    {{ flatpage|parsed_gettext:"content"|safe }}
    </body>
    </html>
