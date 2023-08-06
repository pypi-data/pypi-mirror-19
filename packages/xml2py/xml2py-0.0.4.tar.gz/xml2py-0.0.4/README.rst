
xml2py
======

Convert an xml file or string to a python dict or DotDict.

classes

    * XmlToDict

    * DotDict         

methods

    * dict_load(xml_filename, **kwargs) 
        Convert xml file (path, object, or stream) to dict.

    * dict_loads(xml_string, **kwargs) 
        Convert xml string to dict.

    * dotdict_load(xml_filename, **kwargs)  
        Convert xml file (path, object, or stream) to DotDict.

    * dotdict_loads(xml_string, **kwargs) 
        Convert xml string to DotDict.

    All kwargs are passed to XmlToDict.__init__

    * to_dotdict(obj) 
        Recursively traverse ``obj`` and return an equivalent
        object whose every (non-DotDict) dict is converted to
        a DotDict.

XmlToDict
---------

    python_dict = XmlToDict().element_to_dict(xml_element)

    XmlToDict() == XmlToDict(
            attrib_prefix='_',
            text_key='_text_',
            namespace_pattern=r'\{.*\}',
            namespace_replace='',
            )

An XML tag has a tagname and contains zero or more attributes,
zero or more nested tags, and possibly some text content.

The idea is to use the tagname as a key whose value is a dict
which contains the tag's attributes, nested tags, and text.
The first problem is the potential key clash between attribute
names and nested tagnames, as well as where to store the text.

The solution adopted here is to use the tagname of each nested tag
as its key, and to prepend *attrib_prefix* to each attribute name
as the key for the attribute, and to store the text in *text_key*.
As a special case, if a tag has no attributes, no nested tags,
and only text, then the text is stored as the value of the
tagname.

No checking is done so if there are still key clashes after the
name mangling, then tagname beats *text_key* beats attribute.

The default *attrib_prefix* is '_'
The default *text_key* is '_text_'

The next problem is the interpretation of say::

    <a>
        <b n='1' />
        <c n='2' >TEXT</c>
        <b n='3' />
    </a>

It could be considered a list of three tags, but in converting
this into a dict and knowing that "getElementsByTagName" is often
used while navigating XML, it is converted as::

    {
    'a': {
        'c': {'_n': 2 _text_='TEXT'}, 
        'b': [{'_n': 1}, {'_n': 3}], 
        }
    }

While the order of the <b> tags is preserved, the sequence between
the tags is lost.

Finally, when namespaces are used in the XML document, tagnames 
include the namespace and it is often convenient to replace them 
with something shorter.  *namespace_pattern* is a regular
expression pattern string used to match the tagname.
*namespace_replace* is the replacement string to use::

    tagname = re.sub(namespace_pattern, namespace_replace, tagname)

The default namespace_pattern is r'\{.*\}'
The default namespace_replace is ''
This removes the namespace from the tagname.

DotDict
-------

A DotDict is a dict whose attribute access and item access
are equivalent.  It is convenient for exploring XML files with
the Python interpreter because "dot-notation" is simpler to type
than dict notation.

    dd.x == dd["x"]

On instantiation, ``self`` is traversed recursively and each
(non-DotDict) dict found in it is converted to a DotDict.

Keys which are dict attributes or are unsuitable as attribute
names (e.g. pop, items, 1, $x) can still be used as DotDict
keys, however their values are only accessable using dict
notation.

    >>> assert x == DotDict.to_dotdict(x)
     
    >>> dd = DotDict(x=1)
    >>> dd['x'] == dd.x == 1
    True
    >>> dd.y = 2
    >>> dd['y']
    2
    >>> dd['y'] = 22
    >>> dd.y
    22
    >>> dd.keys()
    ['x', 'y']

**WARNING**
__del__attr__, __getattr__, and __setattr__ are redefined
to operate on ``self`` instead of ``self.__dict__``.
__setattr__ and __delattr__ work as expected, however while
__getattr__ is redefined, __getattribute__ is not.  Since
__getattribute__ only calls __getattr__ if it needs to, dict
built-in methods cannot be over-written.  This is deliberate
but leads to some surprising behavior when a key clashes
with a built-in method:

    >>> dd.update = 'a string'     # set attribute
    >>> dd['update']               # works as expected
    'a string'
    >>> dd.update == dd['update']  # get attribute doesn't find the key
    False                          # 'update' because __getattribute__
    >>> type(dd.update)            # finds the built-in method first.
    <type 'builtin_function_or_method'>

