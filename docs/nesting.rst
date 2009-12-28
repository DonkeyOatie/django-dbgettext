.. _nesting:

Nested Models
=============

If your application uses models which have parent-child relationships, you may wish to set the ``parent`` :ref:`option <options>` to provide a more appropriate file hierarchy and cascading querysets.

For example, if you have a CMS application with a ``Page`` model which may include ``Link`` objects on each page, you could set your ``Link`` ``Options`` like::

    class LinkOptions(Options):
        parent = 'page'  # name of ForeignKey field to Page
        # other options here...

Note that the parent model must also be registered with dbgettext.

This has two benefits:

- child objects will only be translated if their parent is (so, for example, links from an unpublished ``Page`` will not be included if the parent's ``translate-if`` ``Option`` is set appropriately)
- :doc:`dbgettext_export <dbgettext_export>` will append child output to the parent's path. For example: ``locale/dbgettext/cms/page/about_us/contact_us/link_13/`` instead of ``locale/dbgettext/cms/link/link_13/`` -- this provides additional context to the translator

Note that the above example uses a customised ``get_path_identifier`` ``Option`` for ``Page`` to provide nicer a slug-based path (``about_us/contact_us`` instead of ``page_123``).
