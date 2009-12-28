.. _FAQ:

Frequently Asked Questions
==========================

Q: dbgettext strings are showing up in my ``.po`` files, but are not translated when displayed in my browser
    A: Make sure you have:
        - run ``compilemessages``
	- restarted the server
	- used ``gettext`` or ``trans`` to translate the strings in when accessed in your code or templates
