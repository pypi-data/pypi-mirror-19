

SYNOPSIS
--------

.. code::

    modulereport [options]

    modulereport --help


DESCRIPTION
-----------

.. include:: ../longdescription.rst


OPTIONS
-------

To see all options available in your installation, run::

    modulereport --help

All options available as of modulereport v\ |release|::

    positional arguments:
      pathname          path to python file to analyze for imports
    
    optional arguments:
      -h, --help        show this help message and exit
      -s, --skipreport  skip list of all modules
      -l, --loaded      show loaded modules
      -m, --missing     show missing modules
      -V,               show program's version number and exit


EXAMPLES
--------

Show usage::

    modulereport --help

Show program version::

    modulereport -V


SEE ALSO
--------

Module Reporter Homepage: https://github.com/berrak/modulereport

modulereport documentation: https://modulereport.readthedocs.io


BUGS
----

Please report all bugs to https://github.com/berrak/modulereport/issues/
