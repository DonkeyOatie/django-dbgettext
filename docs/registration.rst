.. _registration:

Registering Models
==================

Models can be registered for django-dbgettext in a similar fashion to registering `ModelAdmin classes <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-objects>`_ for ``django.contrib.admin``

Simply create a ``gettext.py`` file within your application root directory, import the dbgettext ``registry`` object, and register your Models together with their customised ``dbgettext.models.Options``. For example::

    from dbgettext.registry import registry, Options
    from myapp.models import MyModel

    class MyModelOptions(Options):
        attributes = ('title',)
	html_attributes = ('body',)
	
    registry.register(MyModel, MyModelOptions)

That's it. Your ``gettext.py`` files will be automatically imported by django-dbgettext, and registered models will be included when running :doc:`dbgettext_export <dbgettext_export>`.


.. _options:

-----------
``Options``
-----------
    
- ``attributes``: 
    tuple of names of fields/callables to be translated
- ``html_attributes``: 
    tuple of names of fields/callables with HTML content which should have 
    translatable content extracted (should not be listed in ``attributes``)
- ``translate_if``:
    dictionary used to ``filter()`` queryset 
- ``get_path_identifier``:
    function returning string used to identify object in path to exported 
    content (given an object)
- ``parent``:
    name of foreign key to parent model, if registered. Affects:
        - path (path_identifier appended onto parent path)
        - queryset (object only translated if parent is)
- ``custom_lexicon_rules``
    list of extra custom rules ((regexp, function) tuples) to be applied when 
    parsing HTML -- see html.py
- ``custom_lexicon``:
    complete list of rules ((regexp, function) tuples) for parsing HTML -- see 
    html.py
