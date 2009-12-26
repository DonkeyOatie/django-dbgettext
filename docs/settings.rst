.. _settings:

Settings
========

The following settings can be overridden in your project's ``settings.py``:

* ``DBGETTEXT_PATH``: path (absolute or relative to project root) where :doc:`dbgettext_export <dbgettext_export>` should store its output. Defaults to ``locale``.
* ``DBGETTEXT_ROOT``: name of directory within ``DBGETTEXT_PATH`` (redundancy to provide protection from auto-purging upon export). Defaults to ``dbgettext``.
* ``DBGETTEXT_INLINE_TAGS``: tuple of tag names allowed to appear inline within strings extracted from ``html_attributes``. Defaults to ``('b','i','u','em','strong',)``.
