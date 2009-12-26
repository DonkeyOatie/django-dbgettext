.. django-dbgettext documentation master file, created by
   sphinx-quickstart on Sat Dec 26 19:39:41 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-dbgettext documentation
==============================

Here lies some basic documentation to get you started with django-dbgettext. The application itself is not overly large or complex, and I recommend perusing the source code for a full understanding.

The premise of django-dbgettext is simple: `gettext <http://www.gnu.org/software/gettext>`_ is already used for translating content from Django's source code and templates, so why not use it for translating database content also? Then the whole process is unified and simplified for translators, and there is no need to provide custom administration interfaces for dynamic content. Simply use the ``dbgettext_export`` `management command <http://docs.djangoproject.com/en/dev/howto/custom-management-commands/>`_ to export the content from the database prior to running `makemessages <http://docs.djangoproject.com/en/dev/topics/i18n/#message-files>`_.



Contents:

.. toctree::
   :maxdepth: 2

   registration
   dbgettext_export
   settings


