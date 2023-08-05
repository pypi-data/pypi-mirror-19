SmartyParse
===========

|Code Climate| |Issue Count| |Build Status|

What is SmartyParse?
~~~~~~~~~~~~~~~~~~~~

SmartyParse is a binary packing/unpacking (aka building/parsing) library
for arbitrary formats written for ``python >= 3.3``. If you have a
defined binary format (.tar, .bmp, byte-oriented network packets, etc)
or are developing one, SmartyParse is a way to convert those formats to
and from Python objects. Its most direct alternative is
`Construct <https://construct.readthedocs.org/en/latest/intro.html>`__,
which is admittedly much more mature.

**As an explicit warning,** this is a very, very new library, and you
are likely to run into some bugs. Pull requests are welcome, and I
apologize for the sometimes messy source.

What makes SmartyParse different?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SmartyParse, first and foremost, was built to support self-describing
formats. Though it is (to an extent) possible to create these in
declarative parsing libraries like Construct, it is very tedious, and
requires a substantial amount of extra code.

Fundamentally that means there are three big differences between
SmartyParse and Construct:

1. SmartyParse is highly Pythonic and very intuitive. Construct requires
   learning a specialized Construct descriptive format.
2. SmartyParse is imperative. Construct is declarative.
3. SmartyParse supports running arbitrary callbacks *during* the parsing
   process.

Otherwise, Construct and SmartyParse are functionally similar (though
for the record, SmartyParse doesn't yet natively support bit-oriented
formats, which Construct does).

Installation
============

Smartyparse is currently in pre-release alpha status. It *is* available
on pip, but you must explicitly allow prerelease versions like this:

::

    pip install --pre smartyparse

Smartyparse has no external dependencies at this time (beyond the
standard library), though building it from source will require pandoc
and pypandoc:

::

    sudo apt-get install pandoc
    pip install pypandoc

Example usage
=============

See
`/docs <https://github.com/Muterra/py_smartyparse/tree/master/docs>`__
for full API documentation.

**Declaring a simple length -> data object:**

+----------+----------+----------------+
| Offset   | Length   | Description    |
+==========+==========+================+
| 0        | 4        | Int32 U, *n*   |
+----------+----------+----------------+
| 4        | *n*      | Blob           |
+----------+----------+----------------+

.. code:: python

    from smartyparse import SmartyParser
    from smartyparse import ParseHelper
    import smartyparse.parsers

    unknown_blob = SmartyParser()
    unknown_blob['length'] = ParseHelper(parsers.Int32(signed=False))
    unknown_blob['data'] = ParseHelper(parsers.Blob())
    unknown_blob.link_length(data_name='data', length_name='length')

**Nesting that to define a simple file:**

+------------------+----------+----------------+
| Offset           | Length   | Description    |
+==================+==========+================+
| 0                | 4        | Magic 'test'   |
+------------------+----------+----------------+
| 4                | 4        | Int32 U, *n*   |
+------------------+----------+----------------+
| 8                | *n*      | Blob           |
+------------------+----------+----------------+
| 8 + *n*          | 4        | Int32 U, *m*   |
+------------------+----------+----------------+
| 12 + *n*         | *m*      | Blob           |
+------------------+----------+----------------+
| 12 + *n* + *m*   | 4        | Int32 U        |
+------------------+----------+----------------+

.. code:: python

    test = SmartyParser()
    test['magic'] = ParseHelper(parsers.Blob(length=4))
    test['blob1'] = unknown_blob
    test['blob2'] = unknown_blob
    test['tail'] = ParseHelper(parsers.Int32(signed=False))

**An object to pack into the above:**

.. code:: python

    test_obj = {
        'magic': b'test',
        'blob1': {
            'data': b'Hello world!'
        },
        'blob2': {
            'data': b'Hello, world?'
        },
        'tail': 123
    }

*Why the awkward dict for the blobs?* Well, because SmartyParser objects
aren't usually intended for things as simple as a length <-> value pair.
It would make a lot more sense if it were 'header' and 'body', wouldn't
it?

**Packing and recycling the above object:**

.. code:: python

    >>> packed = test.pack(test_obj)
    >>> test_obj_reloaded = test.unpack(packed)
    >>> test_obj == test_obj_reloaded
    True

Supporting SmartyParse
======================

Smartyparse is under development as part of the `Muse
protocol <https://github.com/Muterra/doc-muse>`__ implementation used in
the `Ethyr <https://www.ethyr.net>`__ encrypted email-like messaging
application.

Todo
====

(In no particular order)

-  Ensure that smartyparsers can be created without parsers, so that
   callbacks can be registered on them, before their parsers have been
   defined. Basically, avoid all of these incredibly annoying "Nonetype
   has no set\_callback method" issues by allowing on-the-fly parser
   declaration, instead of setting the actual field itself to None.
-  Think about register\_callback vs set\_callback vs add\_callback etc.
   It would be nice to easily and natively support multiple callbacks.
   HOWEVER, there's an argument to be made that this should be handled
   elsewhere, since functions can call other functions.
-  Allow SmartyParsers with a single "visible" object (example: pascal
   strings) to be expanded into parent containers, avoiding the awkward
   double-dict construction
-  Change SmartyParserObject to use slots for storage, but not for item
   names (essentially removing attribute-style access, which isn't
   documented anyways)
-  Add self-describing format to example usage
-  Write .bmp library showcase

   -  https://github.com/construct/construct/blob/master/construct/formats/graphics/bmp.py
   -  https://en.wikipedia.org/wiki/BMP\_file\_format
   -  http://www.dragonwins.com/domains/getteched/bmp/bmpfileformat.htm

-  Move/mirror documentation to readthedocs
-  Add padding generation method (in addition to constant byte)
-  Add pip version badge:
   ``[![PyPi version](https://pypip.in/v/$REPO/badge.png)](https://github.com/Muterra/py_smartyparse)``
   above.
-  Support bit orientation
-  Support endianness of binary blobs (aka transforming from little to
   big)
-  Support memoization of static SmartyParsers for extremely performant
   parsing
-  Support memoization of partially-static smartyparsers for
   better-than-completely-dynamic parsing
-  Autogeneration of integration test suite from API spec in /doc/
-  Random self-describing format declaration and testing
-  Performance testing
-  Add customized `pep8 <http://pep8.readthedocs.org/en/latest/>`__ to
   `codeclimate
   testing <https://docs.codeclimate.com/v1.0/docs/pep8>`__, as per (as
   yet unpublished) Muterra code style guide
-  Change logic to allow for delayed execution on callbacks for
   link\_length so the content parser can be dynamically specified
-  Add utility function for generating a single callback from multiple
   callables

Done!
~~~~~

-  [STRIKEOUT:Add passing of parent SmartyParser to callback system.]
   Added in 0.1a4 with the ``@references(referent)`` decorator.
-  [STRIKEOUT:Clean up callback API.] Added in 0.1a4
-  [STRIKEOUT:Support for "end flags" for indeterminate-length lists]
   Added in 0.1a5

Misc API notes
==============

-  SmartyParser fieldnames currently **must** be valid identifier
   strings (anything you could assign as an attribute). If you want to
   programmatically check validity, use ``'foo'.isidentifier()``, but
   SmartyParser will raise an error if you try to assign an invalid
   fieldname. This is the result of using ``__slots__`` for some memory
   optimization, which is a compromise between default dict behavior and
   memory use. If you're parsing a ton of objects, it will be very
   helpful for memory consumption.
-  Due to numeric imprecision, floats and doubles can potentially break
   equivalence (ie ``start == reloaded``) when comparing the before and
   after of packing -> unpacking the same object.

.. |Code Climate| image:: https://codeclimate.com/github/Muterra/py_smartyparse/badges/gpa.svg
   :target: https://codeclimate.com/github/Muterra/py_smartyparse
.. |Issue Count| image:: https://codeclimate.com/github/Muterra/py_smartyparse/badges/issue_count.svg
   :target: https://codeclimate.com/github/Muterra/py_smartyparse
.. |Build Status| image:: https://travis-ci.org/Muterra/py_smartyparse.svg?branch=master
   :target: https://travis-ci.org/Muterra/py_smartyparse
