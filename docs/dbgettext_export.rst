.. _dbgettext_export:

The ``dbgettext_export`` Management Command
===========================================

To obtain a fresh export of your translatable strings from registered models, simply run::

    python manage.py dbgettext_export

from your project's root directory.

This will create a hierarchy of static files (stored by default in ``<project_root>/locale/dbgettext``, configurable using the ``DBGETTEXT_PATH`` and ``DBGETTEXT_ROOT`` settings) containing the translatable strings. E.g.::

    locale/dbgettext/myapp/mymodel_1/title.py
    locale/dbgettext/myapp/mymodel_1/body.py
    locale/dbgettext/myapp/mymodel_2/title.py
    locale/dbgettext/myapp/mymodel_2/body.py

You can then simply run::

    python manage.py makemessages (...)

as per usual, and these strings will be catalogued for you together with the rest of the translatable strings from your code and templates.

**Note:** the ``<DBGETTEXT_PATH>/<DBGETTEXT_ROOT>`` directory is purged each time ``dbgettext_export`` is run to ensure that old data (e.g. from deleted objects) does not persist in the catalogue.

The paths and names of the static files are intentionally verbose to provide the translator with the context of the string they are translating. You can customise the path using the ``get_path_identifier`` and ``parent`` attributes of the ``Options`` class -- see :doc:`registration`.
