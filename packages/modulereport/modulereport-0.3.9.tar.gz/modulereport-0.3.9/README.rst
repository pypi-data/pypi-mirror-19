modulereport
------------

Description
-----------

Lists the modules imported by python script

Installation
------------

With pip:

::

    $ [sudo] pip install modulereport


Usage
-----

::

    $ modulereport [options]

    $ modulereport --help

All options available of modulereport::

    positional arguments:
      pathname          path to python file to analyze for imports
    
    optional arguments:
      -h, --help        show this help message and exit
      -s, --skipreport  skip list of all modules
      -l, --loaded      show loaded modules
      -m, --missing     show missing modules
      -V,               show program's version number and exit


Documentation (ReadTheDocs)
---------------------------

More information about `Module Reporter <https://modulereport.readthedocs.io/>`_.
