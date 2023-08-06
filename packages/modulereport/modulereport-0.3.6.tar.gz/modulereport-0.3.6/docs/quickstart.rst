Quickstart
==========

List all imported modules in a given python script:

::

    $ modulereport setup.py
    --------------------------------------------------
    Full report:
    --------------------------------------------------
    
      Name                      File
      ----                      ----
    m __future__                /usr/lib/python3.4/__future__.py
    m __main__                  setup.py
    m _ast                      
    m _bisect                   
    m _bootlocale               /usr/lib/python3.4/_bootlocale.py
    m _bz2                      /usr/lib/python3.4/lib-dynload/_bz2.cpython-34m-x86_64-linux-gnu.so
    m _codecs                   
    m _collections              
    m _collections_abc          /usr/lib/python3.4/_collections_abc.py
    m _compat_pickle            /usr/lib/python3.4/_compat_pickle.py
    m _ctypes                   /usr/lib/python3.4/lib-dynload/_ctypes.cpython-34m-x86_64-linux-gnu.so
    ...
    ...
    m warnings                  /usr/lib/python3.4/warnings.py
    m weakref                   /usr/lib/python3.4/weakref.py
    m webbrowser                /usr/lib/python3.4/webbrowser.py
    P xml                       /usr/lib/python3.4/xml/__init__.py
    P xml.parsers               /usr/lib/python3.4/xml/parsers/__init__.py
    m xml.parsers.expat         /usr/lib/python3.4/xml/parsers/expat.py
    P xmlrpc                    /usr/lib/python3.4/xmlrpc/__init__.py
    m xmlrpc.client             /usr/lib/python3.4/xmlrpc/client.py
    m zipfile                   /usr/lib/python3.4/zipfile.py
    m zipimport                 
    m zlib
    
    Missing modules:
    ? _dummy_threading imported from dummy_threading
    ? _frozen_importlib imported from importlib
    ? _sysconfigdata_dm imported from _sysconfigdata
    ? apport_python_hook imported from sitecustomize
    ...
    ...


Show help:
----------

::

    modulereport --help
    usage: modulereport [-h] [-s, --skipreport] [-l, --loaded] [-m, --missing]
                        [-V]
                        pathname
    
    positional arguments:
      pathname          path to python file to analyze for imports
    
    optional arguments:
      -h, --help        show this help message and exit
      -s, --skipreport  skip list of all modules
      -l, --loaded      show loaded modules
      -m, --missing     show missing modules
      -V,               show program's version number and exit


Reference:
----------

Modulereporter use *modulefinder.ModuleFinder* from Python 3 standard library.
Source code for `Lib/modulefinder.py <https://hg.python.org/cpython/file/3.6/Lib/modulefinder.py/>`_.
