from django.conf import settings
from registry import registry
import re

class Token(object):
    """ A categorised chunk of HTML content """

    translatable_types = ('text', 'whitespace',)

    def __init__(self, type, raw):
        self.type = type
        self.raw = raw

    def is_translatable(self):
        if self.type in Token.translatable_types:
            return True


class Tag(Token):
    """ An opening/closing/empty HTML tag """

    gettext_inline_tags = getattr(settings, 'DBGETTEXT_INLINE_TAGS', 
                                   ('b','i','u','em','strong',))

    def __init__(self, type, raw, name, attributes=None):
        super(Tag, self).__init__(type, raw)
        self.name = name
        self.attributes = attributes

    def is_translatable(self):
        return self.name.lower() in Tag.gettext_inline_tags


def html_gettext(obj, attribute, export=False):
    """ Extracts translatable strings from HTML content
    
    Returns original content with ugettext applied to translatable parts.

    If export is True, returns a list of translatable strings only.

    """

    options = registry._registry[type(obj)]
    content = getattr(obj, attribute)

    from django.utils.translation import ugettext as _
    # lazy / string_concat don't seem to work how I want...

    def ignore(scanner, token):
        return Token('ignore', token)

    def open_tag(scanner, token):
        return Tag('open', token, scanner.match.groups()[0])

    def close_tag(scanner, token):
        return Tag('close', token, scanner.match.groups()[0])

    def empty_tag(scanner, token):
        return Tag('empty', token, scanner.match.groups()[0])

    def open_tag_with_attributes(scanner, token):
        return Tag(*(('open', token,) + scanner.match.groups()[:2]))

    def empty_tag_with_attributes(scanner, token):
        return Tag(*(('empty', token,) + scanner.match.groups()[:2]))

    def text(scanner, token):
        return Token('text', token)

    def whitespace(scanner, token):
        return Token('whitespace', token)

    ignored = [
        (r'<!--.*?-->', ignore),
        (r'<script.*?/script>', ignore),
    ]

    custom = getattr(options, 'custom_lexicon_rules', [])

    tags = [
        (r'<\s*/\s*([^>]*?)\s*>', close_tag),
        (r'<\s*([^>]*?)\s*/\s*>', empty_tag),
        (r'<\s*([a-zA-Z]+)\s+([^\s>][^>]*?)\s*>', 
         open_tag_with_attributes),
        (r'<\s*([a-zA-Z]+)\s+([^\s>][^>]*?)\s*/\s*>', 
         empty_tag_with_attributes),
        (r'<\s*([^>]*?)\s*>', open_tag),
    ]

    whitespace = [
        (r'\s+', whitespace),
        (r'&nbsp;', whitespace),
    ]

    text = [
        (r'[^<>]*[^\s<>]', text),
    ]
    
    lexicon = getattr(options, 'custom_lexicon', 
                      ignored + custom + tags + whitespace + text)

    scanner = re.Scanner(lexicon, re.DOTALL)
    tokens, remainder = scanner.scan(content)

    gettext = []
    output = []
    current_string = []

    def token_list_contains_text(token_list):
        for t in token_list:
            if t.type == 'text':
                return True
        return False

    def gettext_from_token_list(token_list):
        """ Process token list into format string, parameters and remainder """
        format, params, remainder = '', {}, ''
        # remove any trailing whitespace
        while token_list[-1].type == 'whitespace':
            remainder = token_list.pop().raw + remainder
        for t in token_list:
            if hasattr(t, 'get_key'): 
                format += '%%(%s)s' % t.get_key()
                params[t.get_key()] = t.raw
            else:
                format += t.raw
        return format, params, remainder

    for t in tokens + [Tag('empty', '', '')]:
        if current_string:
            # in the middle of building a translatable string
            if t.is_translatable():
                current_string.append(t)
            else:
                # end of translatable token sequence, check for text content
                if token_list_contains_text(current_string):
                    format, params, trailing_whitespace = \
                        gettext_from_token_list(current_string)
                    gettext.append(format)
                    try:
                        output.append(_(format) % params)
                    except KeyError:
                        # translator edited placeholder names? Fallback:
                        output.append(format % params)
                    output.append(trailing_whitespace)
                else:
                    # should not be translated, raw output only
                    output.append(''.join([x.raw for x in current_string]))
                # empty for next time:
                current_string = []
                # don't forget current token also:
                output.append(t.raw)
        else:
            # should we start a new translatable string?
            if t.is_translatable() and t.type != 'whitespace':
                current_string.append(t)
            else:
                output.append(t.raw)             

    if export:
        if remainder:
            raise Exception, 'scanner got stuck on: "%s"(...)' % remainder[:10]
        return gettext
    else:
        return ''.join(output)
