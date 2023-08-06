Path and File Examples 
**********************

Local path names::

    /local/path/name

Remote path names in case of RFS - Remote Filesystem::

    //hostname/local/path/name
    
Valid entries - which are equal::
    
    /local/path/name
    ///local///path///name
    /////local/path///name
    /local/foo/../path/bar/../name
    /local/foo/../path/bar/../../what/the/heck/../../../name

Same on Windows including the python abstraction by os.path.normpath::

    /local/path/name
    ///local///path///name
    /////local/path///name
    /local/foo/../path/bar/../name
    /local/foo/../path/bar/../../what/the/heck/../../../name

    \local\path\name
    ...


The following entries are either equal or not as depicted::

    /local/path/name == /local//path//name
    /local/path/name != //local//path//name

The following URI subset is supported::

    file://top/x/y
    file:///top/x/y
    file:////top/x/y
    file://///top/x/y

For code examples refer to:

* `UseCases <UseCases.html#>`_
* `tests <tests.html#>`_


Application examples
********************

The functions are initially designed for the internal requirements based on the authors own projects.
Typical requirements are here generic test case definitions as drop-in units.

* bash-core - https://sourceforge.net/projects/bash-core/
   Location independent normalization of test cases for environments with various
   PATH calculations.

* bash-core-library - https://sourceforge.net/projects/bashcorelib/
   Location independent normalization of testcases for environments with various
   PATH calculations. 

* ePyUnit - https://pypi.python.org/pypi/epyunit
   Location independent normalization of paths for drop-in testcases. 
   
* jsondata - https://pypi.python.org/pypi/jsondata
   Location independent normalization of paths for drop-in testcases. 

* jsoncompute - https://pypi.python.org/pypi/jsoncompute
   Location independent normalization of paths for drop-in testcases. 

* ctysNG - https://sourceforge.net/projects/ctysng/
   Various path calculations on a distributed modular platform.
