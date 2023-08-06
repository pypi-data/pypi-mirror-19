Napoleon - *Marching toward legible docstrings*
===============================================

Updates
-------

As of Sphinx 1.3, the napoleon extension will come packaged with Sphinx
under sphinx.ext.napoleon. ``sphinxcontrib.napoleon2`` provides support
for many more directives. It works best with
`Sphinx-theme <https://github.com/LinxiFan/Sphinx-theme>`__ customized
theme based on readthedocs.org

``sphinxcontrib.napolean2`` is based on
```sphinxcontrib.napolean v0.6.0`` <https://bitbucket.org/RobRuana/sphinx-contrib/src/default/napoleon/>`__,
written by Rob Ruana.

+--------------------+--------------------------------------------------------+
| Style              | Directives                                             |
+====================+========================================================+
| info (blue)        | ``.note, .seealso, .references``                       |
+--------------------+--------------------------------------------------------+
| tip (green)        | ``.tip, .hint, .example``                              |
+--------------------+--------------------------------------------------------+
| warning (orange)   | ``.warning, .caution, .attention, .admonition-todo``   |
+--------------------+--------------------------------------------------------+
| danger (red)       | ``.danger, .error, .important``                        |
+--------------------+--------------------------------------------------------+

Other sphinxcontrib extensions can be found
`here <https://bitbucket.org/RobRuana/sphinx-contrib>`__.

Installation
~~~~~~~~~~~~

::

    pip install sphinxcontrib-napolean2

Then add ``sphinxcontrib.napolean`` to the ``extensions`` list in
``docs/source/conf.py``.

How to add your own directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Refer to ``sphinxcontrib-napolean2/directives.py`` for how to add new
   directives.
-  Add new parser methods to ``sphinxcontrib-napolean2/docstring.py``.
   Refer to lines marked with 'ADDED'.
-  Add ``app.add_directive('example', ExampleDirective)`` to ``setup()``
   function in ``sphinxcontrib-napolean2/__init__.py``
-  Modify ``Sphinx-theme/sass/_theme_rst.sass`` to support the new
   directives in the theme.
-  Original designs are located in
   ``Sphinx-theme/wyrm/sass/wyrm_core/_alert.sass``

Intro
-----

Are you tired of writing docstrings that look like this:

::

    :param path: The path of the file to wrap
    :type path: str
    :param field_storage: The :class:`FileStorage` instance to wrap
    :type field_storage: FileStorage
    :param temporary: Whether or not to delete the file when the File
       instance is destructed
    :type temporary: bool
    :returns: A buffered writable file descriptor
    :rtype: BufferedFileStorage

`ReStructuredText <http://docutils.sourceforge.net/rst.html>`__ is
great, but it creates visually dense, hard to read
`docstrings <http://www.python.org/dev/peps/pep-0287/>`__. Compare the
jumble above to the same thing rewritten according to the `Google Python
Style Guide <http://google.github.io/styleguide/pyguide.html>`__:

::

    Args:
        path (str): The path of the file to wrap
        field_storage (FileStorage): The :class:`FileStorage` instance to wrap
        temporary (bool): Whether or not to delete the file when the File
           instance is destructed

    Returns:
        BufferedFileStorage: A buffered writable file descriptor

Much more legible, no?

Napoleon is a `Sphinx
extension <http://sphinx-doc.org/extensions.html>`__ that enables Sphinx
to parse both
`NumPy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__
and
`Google <http://google.github.io/styleguide/pyguide.html#Comments>`__
style docstrings - the style recommended by `Khan
Academy <https://sites.google.com/a/khanacademy.org/forge/for-developers/styleguide/python#TOC-Docstrings>`__.

Napoleon is a pre-processor that parses
`NumPy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__
and
`Google <http://google.github.io/styleguide/pyguide.html#Comments>`__
style docstrings and converts them to reStructuredText before Sphinx
attempts to parse them. This happens in an intermediate step while
Sphinx is processing the documentation, so it doesn't modify any of the
docstrings in your actual source code files.

Getting Started
---------------

1. Install the napoleon extension:

   ::

       $ pip install sphinxcontrib-napoleon

2. After `setting up Sphinx <http://sphinx-doc.org/tutorial.html>`__ to
   build your docs, enable napoleon in the Sphinx conf.py file:

   ::

       # conf.py

       # Add autodoc and napoleon to the extensions list
       extensions = ['sphinx.ext.autodoc', 'sphinxcontrib.napoleon']

3. Use sphinx-apidoc to build your API documentation:

   ::

       $ sphinx-apidoc -f -o docs/source projectdir

Docstrings
----------

Napoleon interprets every docstring that `Sphinx
autodoc <http://sphinx-doc.org/ext/autodoc.html>`__ can find, including
docstrings on: ``modules``, ``classes``, ``attributes``, ``methods``,
``functions``, and ``variables``. Inside each docstring, specially
formatted `Sections <>`__ are parsed and converted to reStructuredText.

All standard reStructuredText formatting still works as expected.

Docstring Sections
------------------

All of the following section headers are supported:

    -  ``Args`` *(alias of Parameters)*
    -  ``Arguments`` *(alias of Parameters)*
    -  ``Attributes``
    -  ``Example``
    -  ``Examples``
    -  ``Keyword Args`` *(alias of Keyword Arguments)*
    -  ``Keyword Arguments``
    -  ``Methods``
    -  ``Note``
    -  ``Notes``
    -  ``Other Parameters``
    -  ``Parameters``
    -  ``Return`` *(alias of Returns)*
    -  ``Returns``
    -  ``Raises``
    -  ``References``
    -  ``See Also``
    -  ``Warning``
    -  ``Warnings`` *(alias of Warning)*
    -  ``Warns``
    -  ``Yield`` *(alias of Yields)*
    -  ``Yields``

Added in sphinxcontrib-napoleon2:

    -  ``Reference`` *(alias of References)*
    -  ``Tip``
    -  ``Hint``
    -  ``Caution``
    -  ``Attention``
    -  ``Danger``
    -  ``Important``
    -  ``Error``

Google vs NumPy
---------------

Napoleon supports two styles of docstrings:
`Google <http://google.github.io/styleguide/pyguide.html#Comments>`__
and
`NumPy <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__.
The main difference between the two styles is that Google uses indention
to separate sections, whereas NumPy uses underlines.

Google style:

::

    def func(arg1, arg2):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        return True

NumPy style:

::

    def func(arg1, arg2):
        """Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        bool
            Description of return value

        """
        return True

NumPy style tends to require more vertical space, whereas Google style
tends to use more horizontal space. Google style tends to be easier to
read for short and simple docstrings, whereas NumPy style tends be
easier to read for long and in-depth docstrings.

The `Khan
Academy <https://sites.google.com/a/khanacademy.org/forge/for-developers/styleguide/python#TOC-Docstrings>`__
recommends using Google style.

The choice between styles is largely aesthetic, but the two styles
should not be mixed. Choose one style for your project and be consistent
with it.

For full documentation see https://sphinxcontrib-napoleon.readthedocs.io
