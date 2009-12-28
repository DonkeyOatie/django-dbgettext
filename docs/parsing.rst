.. _parsing:

Parsing Content
===============

.. _html:

HTML
----

django-dbgettext comes with HTML parsing functionality out of the box, allowing translatable strings to be extracted from fields with HTML content. To translate an field containing HTML, simply include its name in the ``parsed_attributes`` dictionary of the registered ``Options`` (see :ref:`options`), (together with ``dbgettext.lexicons.html.lexicon``).

The ``DBGETTEXT_INLINE_HTML_TAGS`` :ref:`setting <settings>` can be used to define which HTML tags are allowed to appear within translatable strings. E.g.::

    This <b>string</b> is <i>translatable</i> by <u>default</u>.

The ``custom_lexicon_rules`` :ref:`option <options>` allow the HTML parsing algorithm to be customised to suit your needs. For example, the following ``gettext.py`` file allows images to appear as moveable placeholders in translatable strings::

    from dbgettext.registry import registry, Options
    from dbgettext.parser import Token
    from dbgettext.lexicons import html
    from models import Text
    from django.utils.translation import ugettext as _
    
    class ImageToken(Token):
        """ Allows inline images to be 'translated' as %(image:...)s """
    
    	def __init__(self, raw, src):
	    super(ImageToken, self).__init__('image', raw)
	    self.src = src

	def is_translatable(self):
	    return Token.MAYBE_TRANSLATE

	def get_key(self):
	    return 'image:%s' % self.src


    class LinkToken(Token):
        """ Allows inline links to be translated as %(link:...)s 
    
        Also demonstrates Token 'inner translation' features using get_raw
    	and get_gettext to translate within token itself.
    
        """
    
	def __init__(self, raw, href, content):
	    super(LinkToken, self).__init__('link', raw)
	    self.href = href
	    self.content = content

	def is_translatable(self):
	    return Token.ALWAYS_TRANSLATE

	def get_raw(self):
	    return '<a href="%s">%s</a>' % (_(self.href), _(self.content))

	def get_gettext(self):
	    return [self.href, self.content]

	def get_key(self):
	    return 'link:%s' % self.content  # should sanitize content first


    class TextOptions(Options):
	parsed_attributes = {'body': html.lexicon}

	def image(scanner, token):
	    return ImageToken(token, scanner.match.groups()[0])

	def link(scanner, token):
	    return LinkToken(token, scanner.match.groups()[0],
			      scanner.match.groups()[1],)

	custom_lexicon_rules = [
	    (r'<img[^>]+src="([^"]+)"[^>]*>', image),
	    (r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', link),
	    ]

    registry.register(Text, TextOptions)

Subclassing Token
-----------------

``get_key``
    provide this method if your entire ``Token`` should be be displayed as a placeholder -- e.g. ``%(get_key_output_here)s``

``get_raw``
    provide this method if your ``Token`` requires inner translation -- it should return ``self.raw`` with any inner translatable parts already gettexted

``get_gettext``
    this method should return a list of any translatable strings within your ``Token`` (again, only required for inner translation)


.. _custom_parsing:
    
Other Parsing?
--------------
    
Not using HTML? Want to parse `markdown <http://http://daringfireball.net/projects/markdown/>`_ or something exotic instead? Simply register your own lexicon function like the example provided in ``dbgettext.lexicons.html.py`` (having read ``dbgettext.parser.py`` as well). 
    
Once you've got something you're happy with, you may wish to consider submitting your file for inclusion in ``dbgettext.lexicons``.
    
