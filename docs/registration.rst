.. _registration:

Registering Models
==================

Models can be registered for django-dbgettext in a similar fashion to registering `ModelAdmin classes <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-objects>`_ for ``django.contrib.admin``

Simply create a ``dbgettext_registration.py`` file within your application root directory, import the dbgettext ``registry`` object, and register your Models together with their customised ``dbgettext.models.Options``. For example::

    from dbgettext.registry import registry, Options
    from dbgettext.lexicons import html    
    from myapp.models import MyModel

    class MyModelOptions(Options):
        attributes = ('title',)
	parsed_attributes = {'body': html.lexicon}
	
    registry.register(MyModel, MyModelOptions)

That's it. Your ``dbgettext_registration.py`` files will be automatically imported by django-dbgettext, and registered models will be included when running :doc:`dbgettext_export <dbgettext_export>`.

You can customise the module name using the ``DBGETTEXT_REGISTRATION_MODULE_NAME`` :ref:`setting <settings>`.

.. _project-level:

--------------------------
Project-level Registration
--------------------------

To register models from third-party applications, you can specify a module containing dbgettext registration in the ``DBGETTEXT_PROJECT_OPTIONS`` :ref:`setting <settings>`. For example, the following could be stored in ``my_project/dbgettext_options.py`` and ``DBGETTEXT_PROJECT_OPTIONS`` set to ``my_project.dbgettext_options`` to register ``flatpages`` ::

    from dbgettext.registry import registry, Options
    from dbgettext.lexicons import html
    from django.contrib.flatpages.models import FlatPage

    class FlatPageOptions(Options):
	attributes = ('title',)
	parsed_attributes = {'content': html.lexicon}

    registry.register(FlatPage, FlatPageOptions)

.. _options:

-----------
``Options``
-----------
    
- ``attributes``: 
    tuple of names of fields/callables to be translated
- ``parsed_attributes``: 
    dictionary of names of fields/callables with HTML content which should have 
    translatable content extracted (should not be listed in ``attributes``). 
    Values are callables which take an ``Options`` argument and return a 
    lexicon suitable for ``re.Scanner`` -- see ``dbgettext.lexicons.html`` 
    for an example.
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
    parsing
