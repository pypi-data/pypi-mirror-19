===========================================================================
modulereport documentation quick start guide
===========================================================================

This file provides a quick guide on how to compile the documentation.


Setup the environment
---------------------

To compile the documentation you need Sphinx Python library. To install it
and all its dependencies run::

    pip install Sphinx
    pip install sphinx_rtd_theme
    

Compile the html documentation
------------------------------

To compile the documentation (to HTML output) run the following command
from this dir::

    make html

Documentation will be generated inside the ``_build/html`` dir.


View the html documentation
---------------------------

To view the documentation, load ``_build/html/index.html`` in your browser.


Compile the man pages
---------------------

To compile the documentation to system man pages run the following command
from this dir::

    make man

Documentation will be generated (in man format) inside the ``_build/man`` dir.


View the generated man pages
----------------------------

To view the man pages::

    cd _build/man
    man ./modulereport.1


Start over
----------

To cleanup all generated documentation files and start from scratch run::

    make clean

Keep in mind that this command won't touch any documentation source files.
