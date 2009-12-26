class Options(object):
    """
    Encapsulates dbgettext options for a given model 

    - attributes: 
        tuple of names of fields/callables to be translated
    - html_attributes: 
        tuple of names of fields/callables with HTML content which should have 
        translatable content extracted (should not be listed in attributes)
    - translate_if:
        dictionary used to filter() queryset 
    - get_path_identifier:
        function returning string used to identify object in path to exported 
        content (given an object)
    - parent:
        name of foreign key to parent model, if registered. Affects:
        - path (path_identifier appended onto parent path)
        - queryset (object only translated if parent is)
    - custom_lexicon_rules
        list of extra custom rules ((regexp, function) tuples) to be applied
        when parsing HTML -- see html.py
    - custom_lexicon:
        complete list of rules ((regexp, function) tuples) for parsing HTML 
         -- see html.py

    """

    attributes = ()
    html_attributes = ()
    translate_if = {}
    parent = None
    
    def get_path_identifier(self, obj):
        return '%s_%d' % (obj._meta.object_name, obj.id)
